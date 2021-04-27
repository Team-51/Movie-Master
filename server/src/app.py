from flask import Flask, send_from_directory, request, jsonify, session, redirect, url_for
from mysql.connector import connect
from dotenv import load_dotenv
import json, os
import traceback
import copy

load_dotenv()

tempConf = {
    'host': 'localhost',
    'user': '',
    'password': '', 
}
db_name = "movie-master"
userdb = None

# Create app Instance
app = Flask(__name__, static_url_path='/../../client/public')

@app.route("/")
def base():
    return send_from_directory('../../client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('../../client/public', path)

@app.route('/login', methods = ['POST'])
def login():
    # Login the user into mysql database

    name = request.form['username']
    passw = request.form['password']

    if session['logged_in'] == True:
        return 'ALREADY LOGGED IN'

    conf = copy.deepcopy(tempConf)
    conf['user'] = name
    conf['password'] = passw;

    try:
        userdb = connect(**conf)
        session['logged_in'] = True
        session['cred'] = conf
        return 'SUCCESS'
    except:
        return 'FAILED'

@app.route('/register', methods=['POST'])
def register():

    # Register a new user
    # TODO : add type of users as an input for views in grants

    cu = admindb.cursor()

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    try:
        cu.execute(f"""CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}';""")
        cu.execute(f"""INSERT INTO `{db_name}`.User (UserName, Email) VALUES ('{username}', '{email}');""")
        admindb.commit()
        return 'SUCCESS'
    except:
        admindb.rollback()
        return 'FAILED'

@app.route('/logout')
def logout():

    session['logged_in'] = False
    session['cred'] = None
    return "Success"

@app.route('/test')
def test():
    # Ignore
    try:
        userdb = connect(**session['cred'])
        cu = userdb.cursor()
        return "Success"
    except:
        return "Failed"


@app.route("/sql/<string:query>")
def query(query):

    if session['loggen_in'] == False:
        return 'NOT LOGGED IN'

    userdb = connect(**session['cred'])
    cu = sqldb.cursor()

    res = cu.execute(f'{query};', multi=True)

    data = {}
    indexOuter = 0
    for r in res:
        data[indexOuter] = {}
        index = 0
        for row in r:
            data[indexOuter][index] = row
            index += 1

        indexOuter += 1

    sqldb.commit()

    return jsonify(data)

if __name__ == '__main__':
    
    # Admin conf
    conf = copy.deepcopy(tempConf)
    conf['user'] = os.getenv('MYSQL_USER')
    conf['password'] = os.getenv('MYSQL_PASSWORD')

    try:
        admindb = connect(**conf)
        cu = admindb.cursor()
    except:
        print(f'Cannot connect to Mysql')

    cu.execute(f'USE `{db_name}`;')
    
    admindb.commit()

    app.secret_key = "ice good cream"

    app.run(debug=True)
