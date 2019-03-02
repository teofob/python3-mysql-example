from flask import Flask, render_template
import pymysql
import configparser
import requests

config = configparser.RawConfigParser()
config.read('/home/ec2-user/.my.cnf')

app = Flask(__name__)

class Database(object):
    def __init__(self, config):
        host = config['client']['host']
        user = config['client']['user']
        password = config['client']['password']
        db = "emp"

        self.con = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    db=db,
                    cursorclass=pymysql.cursors.DictCursor
                )
        self.cur = self.con.cursor()

    def list_employees(self):
        self.cur.execute("SELECT first_name, last_name, gender FROM employees")
        result = self.cur.fetchall()

        return result

@app.route('/')
def main():
    a = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone').text

    return "Hi! Go to /emp. You are in {}".format(a)


@app.route('/load')
def load():
    from multiprocessing import Pool
    from multiprocessing import cpu_count

    def f(x):
        i = 10000
        for j in xrange(i):
            x*x*i

    processes = cpu_count()
    pool = Pool(processes)
    pool.map(f, range(processes))

    return "loading"


@app.route('/emp')
def employees():

    def db_query():
        db = Database(config)
        emps = db.list_employees()

        return emps

    res = db_query()

    return render_template('employees.html', result=res, content_type='application/json')

