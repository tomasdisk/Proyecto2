# Aqui se listan los imports
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
from flask_mysqldb import MySQL
from datetime import datetime
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
    #app.logger.info("now: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ", sesion time: " + session['log_update'].strftime("%Y-%m-%d %H:%M:%S"))
    logs = RFID_Api.RFID_getLogsByDate(mysql, datetime.now(), session['log_update']);
    #app.logger.info(logs)

    if logs:
        data['new'] = "true"
        log = logs[0]
        #app.logger.info("picc: " + log['PICC'] + "time: " + log['registrated_at'].strftime("%Y-%m-%d %H:%M:%S"))
        data['picc'] = log['PICC'] # asignar picc del registro obtenido
        session['log_update'] = log['registrated_at']
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

    data = request.values
    #app.logger.info(data)
    if 'picc' in data and 'description' in data and 'count' in data:
        if RFID_Api.RFID_addUser(mysql, data['picc'], data['description'], data['count'], "admin"):
            # renderiza la pagina correspondiente con los parametros que se le pasen
            return redirect(url_for('cow', id=data['picc']))

    return redirect(url_for('home'))

# ruta altenativa sin contenido
@app.route('/newLog', methods = ['POST', 'GET'])
def newLog():

    if request.method == 'POST':
        log = request.values
        app.logger.info("POST\nPICC: " + log["picc"] + "\nDevice: " + log["device"])
        if(RFID_Api.RFID_addLog(mysql, log["picc"], log["device"])):
            app.logger.info("Se cargo el log en la BD")
            return render_template('ok.html')

    if request.method == 'GET':
        log = request.values
        app.logger.info("GET\nPICC: " + log["picc"] + "\nDevice: " + log["device"])
        if(RFID_Api.RFID_addLog(mysql, log["picc"], log["device"])):
            app.logger.info("Se cargo el log en la BD")
            return render_template('ok.html')

    app.logger.info("Hubo un problema al cargar el log en la BD!!")
    return render_template('fail.html')

@app.route('/develop')
def develop():

    return render_template('develop.html')

# ruta de logueo por session sin autentificacion
@app.route('/login')
def login():

    # se guardan los datos en la session
    session['logged'] = True
    session['log_update'] = datetime.now()

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
