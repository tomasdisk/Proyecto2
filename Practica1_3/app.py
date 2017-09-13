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
app.config['MYSQL_USER'] = 'flaskapp1_3_app'
app.config['MYSQL_PASSWORD'] = 'flaskapp'
app.config['MYSQL_DB'] = 'flaskapp1_3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init DB
mysql = MySQL(app)

# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/')
def home():

    # se inicializan los datos para su postarior uso
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
    result = cur.execute("SELECT temp, hum, pres, wind, freq FROM samples ORDER BY id DESC LIMIT 10")
    mysql.connection.commit()
    # si hay resultados clacula los promedios y prepara los datos para ser usados por la vista
    if result > 0:
        res = cur.fetchall()
        x = 0
        for r in res:
            if x == 0:
                session['freq'] = r["freq"]
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
    return render_template('home.html', freq=session['freq'],
    temp_avg=temp_avg, temp_sample=temp_sample,
    hum_avg=hum_avg, hum_sample=hum_sample,
    pres_avg=pres_avg, pres_sample=pres_sample,
    wind_avg=wind_avg, wind_sample=wind_sample)

# ruta altenativa sin contenido
@app.route('/develop')
def develop():

    return render_template('develop.html')



if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(host='0.0.0.0', debug=True)
