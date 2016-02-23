from flask import Flask, render_template, request
import MySQLdb
import time
import json
import os


SQL_DB = os.environ.get('THESIS_DB')
SQL_TABLE = os.environ.get('THESIS_TABLE')
SQL_PW = os.environ.get('SQL_PW')

app = Flask(__name__)
db = MySQLdb.connect(host='localhost', user='root',
                     passwd=SQL_PW, db=SQL_DB)
cur = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    req = request.args.get('time', None)
    if req:
        print req
        cur.execute("""SELECT * FROM {} WHERE datetime >= (NOW() - INTERVAL {})""".format(SQL_TABLE, req))
        data = cur.fetchall()
        arr_send = [[str(time.mktime(i[0].timetuple())), str(int(i[1])), str(int(i[2]))]
                    for i in data]
        data_send = json.dumps(arr_send)
        return data_send
    return render_template('index.html')

#for testing purposes
@app.route('/values', methods=['GET', 'POST'])
def values():
    print 'values'
    req = request.args.get('time', None)
    return render_template('test.html', test=req)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
