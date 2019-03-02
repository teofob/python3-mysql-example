from flask import Flask, render_template
import pymysql
import configparser
import requests
from multiprocessing import Pool
from multiprocessing import cpu_count

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
    try:
        a = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone').text
    except:
        a = "NA"

    return "Hi! Go to /emp. You are in {}".format(a)

def f(x):
    i = 1000
    j = 1000
    k = 1000
    for I in xrange(i):
        for J in xrange(j):
            print I, J
            for K in xrange(k):
                l = x*x

@app.route('/load')
def load():
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

