# Aqui se listan los imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_mysqldb import MySQL
import time
from random import randint
import MySQLdb
import decimal
import random
import datetime

app = Flask(__name__)

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="admin",  # your password
                     db="flaskapp")        # name of the data base

# init DB

def main():
    while True:
        cur = db.cursor()
        query= (float(decimal.Decimal(random.randrange(0, 4090))/100), randint(0, 100), float(decimal.Decimal(random.randrange(0, 1500000))/100), randint(0, 150),datetime.datetime.now())
        print(query)
        cur.execute("INSERT INTO microcontrolador(temperatura,humedad,presion,velocidad_viento,fecha) VALUES(%s, %s, %s, %s, %s)",query)
        db.commit()
        cur.close()
        time.sleep(5) 
        pass

if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    main()
    