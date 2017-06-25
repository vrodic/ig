import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, '../data/data.sqlite'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('IG_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def query_values(table_name, source_id, date, sqlite_date_offset=None):
    date_str = "date(?"
    if sqlite_date_offset:
        date_str += ", '" + sqlite_date_offset + "'"
    date_str += ")"
    query = ("select strftime('%H:%M',time) as time, value "
             "from  " + table_name + " "
                                     "where strftime('%Y-%m-%d',time) = " + date_str + " and source_id=? "
                                                                                       "order by time asc;")
    db = get_db()
    cur = db.execute(query, [date, source_id])

    print(query)

    return cur.fetchall()


def query(query_string, params=[]):
    db = get_db()
    cur = db.execute(query_string, params)
    return cur.fetchall()


@app.route('/dash')
def show_dash():
    home = {}
    data = query("SELECT * FROM temperature WHERE source_id=3 ORDER BY id DESC LIMIT 1")
    home['temperature'] = data[0]['value']
    home['temperature_time'] = data[0]['time']

    data = query("SELECT * FROM humidity WHERE source_id=4 ORDER BY id DESC LIMIT 1")
    home['humidity'] = data[0]['value']
    home['humidity_time'] = data[0]['time']

    local = {}

    return render_template('dash.html', home=home,
                           local=local)


@app.route('/add_sensors_data', methods=['POST'])
def add_sensors_data():
    if not request.json:
        abort(400)

    items = []
    db = get_db()

    for item in request.json:
        data = query("SELECT id FROM source WHERE source_type=? AND type=? AND location_id=?",
                     [item['source_type'], item['type'], item['location_id']])
        source_id = data[0]['id']

        db.execute('INSERT INTO ' + item['type'] +
                   ' (source_id, value, time) VALUES (?, ?, (select current_timestamp))',
                   [source_id, item['value']])
        db.commit()

        items.append(item)

    response = {
        'message': 'ok',
        'items': items
    }

    return jsonify({'response': response}), 201


@app.route('/')
def show_entries():
    db = get_db()

    date = request.args.get('date')
    if date is None:
        date = 'now'

    source_id = request.args.get('source_id')
    if source_id is None:
        source_id = 1

    cur = db.execute("""SELECT * FROM source WHERE id=?""",
                     [source_id])
    source = cur.fetchone()
    table_name = source['type']

    query = ("select strftime('%H:%M',time) as time, value "
             "from  " + table_name + " "
                                     "where strftime('%Y-%m-%d',time) =date(?, '-1 days') and source_id=? "
                                     "order by time asc;")
    print(query)

    entries_prev = query_values(table_name, source_id, date, '-1 days')

    entries = query_values(table_name, source_id, date)

    if not entries_prev:
        entries_prev = entries

    return render_template('graph.html', entries=entries,
                           entries_prev=entries_prev,
                           source=source)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
