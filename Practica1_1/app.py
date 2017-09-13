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
app.config['MYSQL_USER'] = 'flaskapp1_1_user'
app.config['MYSQL_PASSWORD'] = 'flaskapp'
app.config['MYSQL_DB'] = 'flaskapp1_1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)

# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/')
def home(num = 0):

    # verifica si hay un id del ultimo usuario agregado para resaltarlo en la tabla
    if 'num' in session:
        num = session['num']
    app.logger.info(num)

    # crea el Cursor para conectarse con la DB
    cur = mysql.connection.cursor()
    # ejecuta la consulta
    result = cur.execute("SELECT * FROM users ORDER BY id DESC")
    mysql.connection.commit()
    # si hay resultados los guarda en 'users'
    if result > 0:
        users = cur.fetchall()

    # ejecuta la consulta para calcular porcentaje
    result = cur.execute("SELECT (Count(id)* 100 / (SELECT COUNT(*) FROM users)) AS percent FROM users WHERE checked = 1")
    mysql.connection.commit()
    # si hay un resultado le trunca los decimales y lo guarda en 'per'
    if result > 0:
        res = cur.fetchone()
        per = '%.2f'%(res["percent"])
        app.logger.info(per)

    # cierra la coneccion con la DB
    cur.close()

    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('home.html', percent=per, people=users, active=num)

# recibe el formulario de entrada, lo procesa y gurada los datos en la DB
@app.route('/form', methods = ['POST'])
def action_form():

    session['num'] = 0

    if request.method == 'POST':
        # procesa la informacion recibida
        data = request.form
        name = data["name"]
        lastname = data["lastname"]
        email = data["email"]
        checked = False
        if request.form.get("check"):
            checked = True

        # crea el Cursor para conectarse con la DB
        cur = mysql.connection.cursor()
        # ejecuta la consulta
        cur.execute("INSERT INTO users(name, lastname, email, checked) VALUES(%s, %s, %s, %s)", (name, lastname, email, checked))
        # guarda el id del usuario recien registrado
        session['num'] = cur.lastrowid
        # persiste los cambio en la DB
        mysql.connection.commit()
        # cierra la coneccion con la DB
        cur.close()

    return redirect(url_for('home'))

# ruta altenativa sin contenido
@app.route('/develop')
def develop():

    return render_template('develop.html')



if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(debug=True)
