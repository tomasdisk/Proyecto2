# Aqui se listan los imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Config DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tomasdisk'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)


@app.route('/')
def home(num = 0):
    if 'num' in session:
        num = session['num']
    app.logger.info(num)

    # DB Cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users ORDER BY id DESC")
    if result > 0:
        users = cur.fetchall()

    result = cur.execute("SELECT (Count(id)* 100 / (SELECT COUNT(*) FROM users)) AS percent FROM users WHERE checked = 1")
    if result > 0:
        res = cur.fetchone()
        per = '%.2f'%(res["percent"])
        app.logger.info(per)

    #num = cur.lastrowid
    cur.close()

    return render_template('home.html', percent=per, people=users, active=num)



#Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/form', methods = ['POST'])
def action_form():

    session['num'] = 0

    if request.method == 'POST':
        data = request.form
        name = data["name"]
        lastname = data["lastname"]
        email = data["email"]
        checked = False
        if request.form.get("check"):
            checked = True

        # DB Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, lastname, email, checked) VALUES(%s, %s, %s, %s)", (name, lastname, email, checked))
        session['num'] = cur.lastrowid
        mysql.connection.commit()
        cur.close()

        #return home(num)

    #return home()
    return redirect(url_for('home'))

@app.route('/develop')
def develop():

    return render_template('develop.html')




if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(debug=True)
