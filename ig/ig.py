import os
import pymysql.cursors
import dateutil.parser

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
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='wlog',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


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


def query_values(table_name, source_id, date, sqlite_date_offset="0 day"):
    date_str = "date_sub(" + date
    date_str += ", interval " + sqlite_date_offset
    date_str += ")"
    query = ("select time(time) as time, value "
             "from  " + table_name + " "
             "where date(time) = " + date_str + " and source_id=" + str(source_id) +
             " order by time asc;")
    print(query)
    db = get_db().cursor()
    db.execute(query)

    print(query)

    return db.fetchall()


def query(query_string):
    db = get_db().cursor()
    db.execute(query_string)
    return db.fetchall()

def get_last_value(table, source_id):
    q = "SELECT * FROM " + table + " WHERE source_id=" + str(source_id) + " ORDER BY id DESC LIMIT 1"
    return query(q)

@app.route('/dash')
def show_dash():
    home = {}
    data = get_last_value("temperature", 3)
    home['temperature'] = data[0]

    data = get_last_value("humidity", 4)
    home['humidity'] = data[0]

    local = {}
    data = get_last_value("temperature", 5)
    local['temperature'] = data[0]

    data = get_last_value("humidity", 6)
    local['humidity'] = data[0]

    data = get_last_value("pm10", 1)
    local['air'] = data[0]

    data = get_last_value("windspeed", 8)
    local['wind'] = data[0]


    return render_template('dash.html', home=home,
                           local=local)


@app.route('/add_sensors_data', methods=['POST'])
def add_sensors_data():
    if not request.json:
        abort(400)

    items = []
    db = get_db()
    cursor = db.cursor()

    for item in request.json:
        data = query("SELECT id FROM source WHERE source_type='" + item['source_type'] +"' AND type='"+ item['type']+"' AND location_id=" +str(item['location_id']))
        source_id = data[0]['id']

        cursor.execute('INSERT INTO ' + item['type'] +
                   ' (source_id, value, time) VALUES ( ' + str(source_id) + ',' + str(item['value']) +', (select now()))')
        db.commit()

        items.append(item)

    response = {
        'message': 'ok',
        'items': items
    }

    return jsonify({'response': response}), 201


@app.route('/')
def show_entries():
    db = get_db().cursor()

    date = request.args.get('date')
    if date is None:
        date = 'now()'

    source_id = request.args.get('source_id')
    if source_id is None:
        source_id = 1

    db.execute('SELECT * FROM source WHERE id=%d'% int(source_id))
    source = db.fetchone()
    table_name = source['type']


    entries_prev = query_values(table_name, source_id, date, '1 day')

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


@app.template_filter('format_time')
def _jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    format='%d %H:%M'
    return native.strftime(format)
