import json
import os
import time
import operator
from flask import request
from flask import Flask, render_template, session, redirect, url_for, g


from flask import make_response
import mysql.connector
from mysql.connector import errorcode
from operator import itemgetter
import requests

application = Flask(__name__)
app = application


application = Flask(__name__)


app = application
all_pools = []


def get_db_creds():
    db = os.environ.get("DB", None) or os.environ.get("database", None)
    username = os.environ.get("USER", None) or os.environ.get("username", None)
    password = os.environ.get(
        "PASSWORD", None) or os.environ.get("password", None)
    hostname = os.environ.get("HOST", None) or os.environ.get("dbhost", None)
    return db, username, password, hostname


def create_table():

    db, username, password, hostname = get_db_creds()
    table_ddl = 'CREATE TABLE pools(pool_name VARCHAR(100), '
    'status TEXT NOT NULL, phone TEXT, '
    'pool_type TEXT, PRIMARY KEY (pool_name))'

    cnx = ''
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                      host=hostname,
                                      database=db)

    except Exception as exp:
        print(exp)

    cur = cnx.cursor()

    try:
        cur.execute(table_ddl)
        cnx.commit()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

# add information to database
@app.route("/static/add_item", methods=['POST'])
def add_item():

    item_name = request.form['item_name']
    price = request.form['price']
    description = request.form['description']
    date_to_deliver = request.form['date_to_deliver']

    db, username, password, hostname = get_db_creds()
    cnx = ''
    try:
        cnx = mysql.connector.connect(
            user=username, password=password, host=hostname, database=db)
    except Exception as e:
        print(e)

    longhorn_db = ("INSERT INTO longhorn_db (item_name, price, description, date_to_deliver ) VALUES ('%s', '%s', '%s', '%s')"
             % (item_name, price, description, date_to_deliver, ))
    check = ("SELECT item_name FROM longhorn_db")

    cur = cnx.cursor()
    cur.execute(check)
    item_names = [dict(item_name=row[0]) for row in cur.fetchall()]

    cur.execute(longhorn_db)
    cnx.commit()
    return render_template('longhorn_db_added.html')


@app.route("/longhorn_db")
def get_pools():

    longhorn_db = {}
    #longhorn_db['item_name'] = 'Barton Springs'
    #longhorn_db['description'] = '832-267-4779'
    #longhorn_db['price'] = 'Open'
    #longhorn_db['date_to_deliver'] = 'Open'
    # print(all_longhorn_db.append(longhorn_db))
    # print(json.dumps(all_longhorn_db))
    # return json.dumps(all_longhorn_db)
    db, username, password, hostname = get_db_creds()
    cnx = ''
    try:
        cnx = mysql.connector.connect(
            user=username, password=password, host=hostname, database=db)
    except Exception as e:
        print(e)

    action = ("SELECT item_name, price, description, date_to_deliver FROM longhorn_db")

    cur = cnx.cursor()
    cur.execute(action)

    data = cur.fetchall()
    print(data)
    all_longhorn_db = []

    # return 'longhorn_db with name %s does not exist' % item_name,404
    for row in data:

        ret_val = {"item_name": row[0],
                   "price": row[1],
                   "description": row[2],
                   "date_to_deliver": row[3]
                   }
        all_longhorn_db.append(ret_val)
    print(all_longhorn_db)

    return json.dumps(all_longhorn_db)
# create the user


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User:{ self.username}>'


users = []
users.append(User(id=1, username='william', password='password'))
users.append(User(id=2, username='sdfe', password='password'))
app.secret_key = 'superscretkey비밀번호'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/', methods=["GET", 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]

        except:
            return redirect(url_for('login'))
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('pool_info_website'))

        return redirect(url_for('login'))

    return render_template('login.html')


# default page
@app.route("/homepage")
def pool_info_website():
    print(g.user)
    if not g.user:
        return redirect(url_for('login'))
    return render_template('index.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
    create_table()
