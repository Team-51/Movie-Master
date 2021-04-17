from flask import Flask, send_from_directory, request, jsonify
from mysql.connector import connect
from dotenv import load_dotenv
import json, os

load_dotenv()

conf = {
    'host': os.getenv('MYSQL_HOST') or 'localhost',
    'user': os.getenv('MYSQL_USER') or '',
    'password': os.getenv('MYSQL_PASSWORD') or 'password'
}
db_name = "movie-master"

# Create app Instance
app = Flask(__name__, static_url_path='/../../client/public')

@app.route("/")
def base():
    return send_from_directory('../../client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('../../client/public', path)

@app.route("/sql/<string:query>")
def query(query):
    # very unsafe sql injection attack
    cu = db.cursor()
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

    db.commit()

    return jsonify(data)

if __name__ == '__main__':
    
    try:
        db = connect(**conf)
        cu = db.cursor()
    except Exception:
        print(f'Cannot connect to Mysql')

    cu.execute(f'USE `{db_name}`;')
    
    db.commit()

    app.run(debug=True)
