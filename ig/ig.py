import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

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


@app.route('/')
def show_entries():
    db = get_db()

    date = request.args.get('date')
    if date is None:
        date = 'now'

    source_id = request.args.get('source_id')
    if source_id is None:
        source_id = 1

    cur = db.execute("""SELECT type  FROM source WHERE id=?""",
                     [source_id])
    table_name = cur.fetchone()['type']

    query = ("select strftime('%H %M',time) as time, value "
             "from  " + table_name + " "
             "where strftime('%Y-%m-%d',time) =date(?, '-1 years') and source_id=? "
             "order by time asc;")
    print(query)

    cur = db.execute(query, [date, source_id])
    entries_prev = cur.fetchall()

    query = ("select strftime('%H %M',time) as time, value "
             "from  " + table_name + " "
             "where strftime('%Y-%m-%d',time) =date(?) and source_id=? "
             "order by time asc;")

    cur = db.execute(query, [date, source_id])

    entries = cur.fetchall()

    if not entries_prev:
        entries_prev = entries

    return render_template('graph.html', entries=entries, entries_prev=entries_prev)


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
