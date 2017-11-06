# Aqui se listan los imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Config DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tomasdisk'
app.config['MYSQL_DB'] = 'RFID_BD'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)

# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/')
def home():


    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('5.html')

# recibe la peticion de nuevos datos por AJAX y los devuelve como JSON
@app.route('/refreshData', methods = ['GET'])
def refreshData():

    if True:
        data['new'] = "true"
        return jsonify(data)
    else:
        data['new'] = "false"
        return jsonify(data)

# ruta que recibe el formulario para cambiar la frecuencia de muestreo
@app.route('/cow/<int:id>', methods = ['GET'])
def cow(id):
    # crea el Cursor para conectarse con la DB
    cur = mysql.connection.cursor()
    # ejecuta la consulta buscando las 10 ultimas muestras para la frecuencia dispuesta por el usuario
    s = "SELECT * FROM users WHERE id = " + str(id)
    result = cur.execute(s)
    #result = cur.execute("SELECT temp, hum, pres, wind FROM samples ORDER BY id DESC LIMIT 10")
    mysql.connection.commit()
    # si hay resultados clacula los promedios y prepara los datos para ser usados por la vista
    if result > 0:
        cow = cur.fetchone()
        PICC = cow["PICC"]
        description = cow["description"]
        count = cow["count"]

    return render_template('cow.html', PICC=PICC, description=description, count=count)

# ruta altenativa sin contenido
@app.route('/newLog', methods = ['POST'])
def newLog():
    PICC = request.form.keys()[0]
    app.logger.info(PICC)
    cur = mysql.connection.cursor()
    s = 'INSERT INTO logs(PICC, device) VALUES ("'+ PICC +'", 5)'
    app.logger.info(s)
    # ejecuta la consulta que guarda los datos en la BD
    cur.execute(s)
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()

    return render_template('5.html')


@app.route('/develop')
def develop():

    return render_template('develop.html')


if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(port=8002, host='0.0.0.0', debug=True)
