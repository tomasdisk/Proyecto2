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
app.config['MYSQL_USER'] = 'flaskapp2_app'
app.config['MYSQL_PASSWORD'] = 'flaskapp'
app.config['MYSQL_DB'] = 'flaskapp2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)

# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/')
def home():

    # se inicializan los datos para su postarior uso
    if 'freq' in session:
        freq = session['freq']
    else:
        freq = 1
    temp_avg = 0
    temp_sample = 0
    hum_avg = 0
    hum_sample = 0
    pres_avg = 0
    pres_sample = 0
    wind_avg = 0
    wind_sample = 0

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
                temp_sample = r["temp"]
                hum_sample = r["hum"]
                pres_sample = r["pres"]
                wind_sample = r["wind"]
            temp_avg += r["temp"]
            hum_avg += r["hum"]
            pres_avg += r["pres"]
            wind_avg += r["wind"]
            x += 1
        temp_avg /= x
        hum_avg /= x
        pres_avg /= x
        wind_avg /= x

    # cierra la coneccion con la DB
    cur.close()

    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('home.html', freq=freq,
    temp_avg=temp_avg, temp_sample=temp_sample,
    hum_avg=hum_avg, hum_sample=hum_sample,
    pres_avg=pres_avg, pres_sample=pres_sample,
    wind_avg=wind_avg, wind_sample=wind_sample)

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
    cur.execute("DELETE FROM config WHERE id = %s", (str(session['id'])))
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
    app.run(host='0.0.0.0', debug=True)
