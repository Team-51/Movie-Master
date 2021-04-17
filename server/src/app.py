from flask import Flask, send_from_directory, request, jsonify, session, redirect, url_for
from mysql.connector import connect
from dotenv import load_dotenv
import json, os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

conf = {
    'host': os.getenv('MYSQL_HOST') or 'localhost',
    'user': os.getenv('MYSQL_USER') or '',
    'password': os.getenv('MYSQL_PASSWORD') or 'password'
}
db_name = "movie-master"

# Create app Instance
app = Flask(__name__, static_url_path='/../../client/public')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods = ['POST'])
def home():

    name = request.form['username']
    passw = request.form['password']

    # TODO check if already logged in

    try:
        data = User.query.filter_by(username=name, password=passw).first()
        if data is not None:
            session['logged_in'] = True
            # TODO find url to redirect
            return 'Login Success'
        else:
            return 'Login Failed'
    except:
        return 'Failed'

@app.route('/register', methods=['POST'])
def register():
    try:
        new_user = User(
            username=request.form['username'],
            password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return 'USER ADDED'
    except:
        return 'FAILED'

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return "Success"

@app.route("/")
def base():
    return send_from_directory('../../client/public', 'index.html')

#app.route("/<path:path>")
#def home(path):
#    return send_from_directory('../../client/public', path)

@app.route("/sql/<string:query>")
def query(query):
    # very unsafe sql injection attack
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
    
    try:
        sqldb = connect(**conf)
        cu = sqldb.cursor()
    except Exception:
        print(f'Cannot connect to Mysql')

    cu.execute(f'USE `{db_name}`;')
    
    sqldb.commit()

    db.create_all()
    app.secret_key = "ice good cream"

    app.run(debug=True)
