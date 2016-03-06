from flask import Flask, render_template, request, flash
from flask.ext.bootstrap import Bootstrap
import MySQLdb
import time
import json


SQL_DB = 'thesis'
SQL_TABLE = 'power'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'null'
bootstrap = Bootstrap(app)
db = MySQLdb.connect(host='localhost', user='root',
                     passwd='raspberry', db=SQL_DB)
cur = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    req = request.args.get('time', None)
    if req:
        cur.execute(
            """SELECT * FROM {} WHERE datetime >= (NOW() - INTERVAL {})"""
            .format(SQL_TABLE, req))
        data = cur.fetchall()
        arr_send = [[str(time.mktime(row[0].timetuple())),
                     str(int(row[1])),
                     str(int(row[2]))]
                    for row in data]
        data_send = json.dumps(arr_send)
        return data_send
    flash(
        'Current threshold: {}'
        .format(int(json.loads(init_gui())['thresh'])))
    return render_template('index.html')

@app.route('/setvals', methods=['GET', 'POST'])
def set_config():
    recv_conf = {key: val for key, val in request.form.items()}
    with open('data/gui.conf', 'r') as f:
        prev_data = json.loads(f.read())
    if prev_data != recv_conf:
        with open('data/gui.conf', 'w') as f:
            f.write(json.dumps(recv_conf))
    return ('', 204)

@app.route('/initvals', methods=['GET', 'POST'])
def init_gui():
    with open('data/gui.conf', 'r') as f:
        ret_conf = json.loads(f.read())
    return json.dumps(ret_conf)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
