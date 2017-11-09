# Aqui se listan los imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
from flask_mysqldb import MySQL
from datetime import date, datetime
import RFID_Api

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

    logs = RFID_Api.RFID_getAllLogs(mysql);

    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('home.html', logs=logs)

# recibe la peticion de nuevos datos por AJAX y los devuelve como JSON
@app.route('/refreshData', methods = ['GET'])
def refreshData():

    data = {
        'new' : "",
        'known': "",
        'picc': "",
        }
    # TODO obtener regitro nuevo si lo hay
    if True:
        data['new'] = "true"
        data['picc'] = "picc" # asignar picc del registro obtenido
        if RFID_Api.RFID_getUserByPicc(mysql, data['picc']):
            data['known'] = "true"
        else:
            data['known'] = "false"
        return jsonify(data)
    else:
        data['new'] = "false"
        return jsonify(data)

# ruta que muestra el perfil de un usuario(vaca)
@app.route('/cow/<string:id>', methods = ['GET'])
def cow(id):

    cow = RFID_Api.RFID_getUserByPicc(mysql, id)
    if cow:
        logs = RFID_Api.RFID_getLogsByPicc(mysql, id)
        return render_template('cow.html', cow=cow, logs=logs)

    return redirect(url_for('home'))

# ruta con formulario para cargar un nuevo usuario(vaca)
@app.route('/newCow', methods=['GET', 'POST'])
def newCow():

    data = request.values
    if 'picc' in data:
        picc = data["picc"]
        # renderiza la pagina correspondiente con los parametros que se le pasen
        return render_template('newCow.html', picc=picc)

    return redirect(url_for('home'))


# ruta que procesa el formulario de un nuevo usuario(vaca)
@app.route('/newCow/form', methods = ['POST'])
def newCowForm():

    app.logger.info(request.form.keys())
    app.logger.info(request.form.values())
    # TODO flata procesar el formulario y volcarlo en la BD

    # renderiza la pagina correspondiente con los parametros que se le pasen
    return render_template('ok.html')

# ruta altenativa sin contenido
@app.route('/newLog', methods = ['POST'])
def newLog():

    PICC = request.form.keys()[0]
    app.logger.info(PICC)
    if(RFID_Api.RFID_addLog(mysql, PICC, 1)):
        app.logger.info("Se cargo el log en la BD")
        return render_template('ok.html')
    else:
        app.logger.info("Hubo un proble al cargar el log en la BD!!")
        return render_template('fail.html')

@app.route('/develop')
def develop():

    return render_template('develop.html')

# ruta de logueo por session sin autentificacion
@app.route('/login')
def login():

    # se guardan los datos en la session
    session['logged'] = True

    return redirect(url_for('home'))

# ruta de salida que cierra la session
@app.route('/logout')
def logout():

    # se limpia la session
    session.clear()
    session['logged'] = False

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key='12345'
    # Define HOST y PUERTO para accerder
    # app.run(host='localhost', port=80)
    app.run(port=8002, host='0.0.0.0', debug=True)