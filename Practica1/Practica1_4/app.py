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
app.config['MYSQL_USER'] = 'flaskapp1_4_app'
app.config['MYSQL_PASSWORD'] = 'flaskapp'
app.config['MYSQL_DB'] = 'flaskapp1_4'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)

# funcion que busca en la BD los datos y los procesa para ser mostrados por la vista
def get_data(freq):

    # se inicializan los datos para su postarior uso
    data = {
            'temp_avg' : 0,
            'temp_sample' : 0,
            'hum_avg' : 0,
            'hum_sample' : 0,
            'pres_avg' : 0,
            'pres_sample' : 0,
            'wind_avg' : 0,
            'wind_sample' : 0,
        }

    # crea el Cursor para conectarse con la DB
    cur = mysql.connection.cursor()
    # ejecuta la consulta buscando las 10 ultimas muestras para la frecuencia dispuesta por el usuario
    s = "SELECT temp, hum, pres, wind FROM samples WHERE (freq MOD "+ str(freq) +" = 0) ORDER BY id DESC LIMIT 10"
    result = cur.execute(s)
    #result = cur.execute("SELECT temp, hum, pres, wind FROM samples ORDER BY id DESC LIMIT 10")
    mysql.connection.commit()
    # si hay resultados clacula los promedios y prepara los datos para ser usados por la vista
    if result > 0:
        res = cur.fetchall()
        x = 0
        for r in res:
            if x == 0:
                data['temp_sample'] = r["temp"]
                data['hum_sample'] = r["hum"]
                data['pres_sample'] = r["pres"]
                data['wind_sample'] = r["wind"]
            data['temp_avg'] += r["temp"]
            data['hum_avg'] += r["hum"]
            data['pres_avg'] += r["pres"]
            data['wind_avg'] += r["wind"]
            x += 1
        data['temp_avg'] /= x
        data['hum_avg'] /= x
        data['pres_avg'] /= x
        data['wind_avg'] /= x

    # cierra la coneccion con la DB
    cur.close()

    return data

# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/')
def home():

    # se revisa si hay una frecuencia seteada
    if 'freq' in session:
        freq = session['freq']
    else:
        freq = 1
    # se cargan los datos
    data = get_data(freq)

    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('home.html', freq=freq, data=data)

# recibe la peticion de nuevos datos por AJAX y los devuelve como JSON
@app.route('/refreshData', methods = ['GET'])
def refreshData():

    if 'freq' in session:
        freq = session['freq']
    else:
        freq = 1

    data = get_data(freq)
    data['temp_sample'] = str(data['temp_sample'])
    data['hum_sample'] = str(data['hum_sample'])
    data['pres_sample'] = str(data['pres_sample'])
    data['wind_sample'] = str(data['wind_sample'])
    data['temp_avg'] = str(data['temp_avg'])
    data['hum_avg'] = str(data['hum_avg'])
    data['pres_avg'] = str(data['pres_avg'])
    data['wind_avg'] = str(data['wind_avg'])

    return jsonify(data)

# recibe el formulario que define si apagar o encender el microcontrolados y la lectura de muestras
@app.route('/form_power', methods = ['POST'])
def action_form_power():

    if session['power'] == 0:
        session['power'] = 1
    else:
        session['power'] = 0

    # crea el Cursor para conectarse con la DB
    cur = mysql.connection.cursor()
    # ejecuta la consulta guardando para el usuario la accion apagar/encender
    cur.execute("UPDATE config SET power = %s WHERE id = %s", (session['power'], session['id']))
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()

    return redirect(url_for('home'))

# funcion que almacena la frecuencia de muestreo solicitada por el usuario en la BD
def change_freq(freq):
    cur = mysql.connection.cursor()
    # ejecuta la consulta
    cur.execute("UPDATE config SET freq = %s WHERE id = %s", (freq, session['id']))
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()
    return

# ruta que recibe el formulario para cambiar la frecuencia de muestreo
@app.route('/form_sense/<int:freq>', methods = ['POST'])
def action_form_sense(freq):
    if freq == 1 or freq == 5 or freq == 10 or freq == 20 or freq == 40:
        session['freq'] = freq
        change_freq(freq)
    return redirect(url_for('home'))

# ruta altenativa sin contenido
@app.route('/develop')
def develop():

    return render_template('develop.html')

# ruta de logueo en la que se crea automaticamente un usuario para la session actual donde se persiste su informacion en la BD
@app.route('/login')
def login():

    # se guardan los datos en la session
    session['logged'] = True
    session['user'] = 'admin'
    session['power'] = 1
    session['freq'] = 5

    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    cur.execute("INSERT INTO config(user, power, freq) VALUES (%s, %s, %s)", (session['user'], 1, 5))
    # guarda el id del usuario recien registrado
    session['id'] = cur.lastrowid
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()

    return redirect(url_for('home'))

# ruta de salida que elimina el usuario tanto de la session como de la BD
@app.route('/logout')
def logout():

    cur = mysql.connection.cursor()
    # ejecuta la consulta para eluminar usuario
    s = "DELETE FROM config WHERE id = " + str(session['id'])
    cur.execute(s)
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()

    # se limpia la session
    session.clear()
    session['logged'] = False

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(host='localhost', port=8002, debug=True)
