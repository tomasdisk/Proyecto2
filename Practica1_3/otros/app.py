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


@app.route('/')
def home():

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
    # ejecuta la consulta
    s = "SELECT temp, hum, pres, wind FROM samples WHERE (freq MOD "+ str(freq) +" = 0) ORDER BY id DESC LIMIT 10"
    app.logger.info(s)
    result = cur.execute(s)
    #result = cur.execute("SELECT temp, hum, pres, wind FROM samples ORDER BY id DESC LIMIT 10")
    # si hay resultados los guarda en 'users'
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


# Define la ruta y metodo con el que se debe llegar a este endpoint
@app.route('/form_power', methods = ['POST'])
def action_form_power():

    if session['power'] == 0:
        session['power'] = 1
    else:
        session['power'] = 0

    # crea el Cursor para conectarse con la DB
    cur = mysql.connection.cursor()
    # ejecuta la consulta
    cur.execute("UPDATE config SET power = %s WHERE user = %s", (session['power'], session['user']))
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()

    return redirect(url_for('home'))


def change_freq(freq):
    cur = mysql.connection.cursor()
    # ejecuta la consulta
    cur.execute("UPDATE config SET freq = %s WHERE user = %s", (freq, session['user']))
    # persiste los cambio en la DB
    mysql.connection.commit()
    # cierra la coneccion con la DB
    cur.close()
    return

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

@app.route('/login')
def login():

    session['logged'] = True
    session['user'] = 'admin'
    session['power'] = 1
    session['freq'] = 5

    return redirect(url_for('home'))

@app.route('/logout')
def logout():

    session.clear()
    session['logged'] = False

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(debug=True)
