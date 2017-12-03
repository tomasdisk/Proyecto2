from datetime import date

_admin_pass = "admin"

# la idea original es que un usuario tenga asociados varios PICCs de una tabla de PICCs, pero por ahora cada usuario tiene un solo PICC almacenado con sus datos.

# las funciones necesitan recibir la coneccion con la BD para operar (parametro 'mysql').

# Los IDs no pueden ser numeros negativos!

###--------------------------------------------------------------------------###
### Access to information ###

# Users

#ok
def RFID_getAllUsers(mysql):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM users")
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getUser(mysql, userId):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM users WHERE id = %s", str(userId))
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok de momento usa el picc interno de la tabla user
def RFID_getUserByPicc(mysql, picc):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM users WHERE PICC = %s", [picc])
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getLastUser(mysql):
    # busca el ultimo log
    log = RFID_getLastLog(mysql)
    if log == 0:
        return 0
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM users WHERE PICC = %s", [log["PICC"]])
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

# PICCs (de momento cada user tiene un PICC el cual se guarda en su misma tabla)

def RFID_getAllPiccs(mysql):
    pass

def RFID_getPicc(mysql, piccId):
    pass

def RFID_getIdsByUser(mysql, user):
    pass

def RFID_getLastPicc(mysql):
    pass

# Devices

#ok
def RFID_getAllDevices(mysql):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM devs")
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getDevice(mysql, deviceId):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM devs WHERE id = %s", str(deviceId))
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

# Logs

#ok
def RFID_getAllLogs(mysql):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs")
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getLog(mysql, logId):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs WHERE id = %s", str(logId))
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getLogsByUser(mysql, userId):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs WHERE PICC = (SELECT PICC FROM users WHERE id = %s)", str(userId))
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getLogsByPicc(mysql, picc):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs WHERE PICC = %s", [picc])
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

#ok
def RFID_getLastLog(mysql):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 1")
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchone()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0
#ok
def RFID_getLogsByDate(mysql, beginDate, endDate = date.min):
    # crea un cursor a la base de datos
    cur = mysql.connection.cursor()
    # ejecuta la consulta que guarda los datos en la BD
    r = cur.execute("SELECT * FROM logs WHERE %s < registrated_at AND registrated_at < %s", (endDate, beginDate))
    # persiste los cambio en la DB
    mysql.connection.commit()

    if r > 0:
        # obtengo los datos
        data = cur.fetchall()
        # cierra la coneccion con la DB
        cur.close()
        return data
    else:
        cur.close()
        return 0

###--------------------------------------------------------------------------###
### Administation tools ###

def RFID_changeAdminPass(oldPass, newPass):
    if oldPass == _admin_pass:
        _admin_pass = newPass
        return 1
    return 0

# Users

def RFID_addUser(mysql, picc, description, count, password):
    try:
        if password == "admin":
            cur = mysql.connection.cursor()
            # ejecuta la consulta que guarda los datos en la BD
            cur.execute("INSERT INTO users(PICC, description, count) VALUES (%s, %s, %s)", (picc, description, str(count)))
            # persiste los cambio en la DB
            mysql.connection.commit()
            # cierra la coneccion con la DB
            cur.close()
            return 1
        return 0
    except Exception as e:
        return 0

def RFID_delUser():
    pass

# PICCs

def RFID_addPicc():
    pass

def RFID_delPicc():
    pass

# Devices

def RFID_addDevice():
    pass

def RFID_delDevice():
    pass

# Logs

def RFID_delLogsByUser():
    pass

def RFID_delLogsByDate():
    pass

def RFID_delAllLogs():
    pass

def RFID_executeQuery(mysql, query, password):
    try:
        if password == _admin_pass:
            # crea un cursor a la base de datos
            cur = mysql.connection.cursor()
            # ejecuta la consulta que guarda los datos en la BD
            r = cur.execute("SELECT * FROM users")
            # persiste los cambio en la DB
            mysql.connection.commit()

            if r > 0:
                # obtengo los datos
                data = cur.fetchall()
                # cierra la coneccion con la DB
                cur.close()
                return data

            cur.close()
        return 0
    except Exception as e:
        return 0

###--------------------------------------------------------------------------###
### Devices tools ###

#ok
def RFID_addLog(mysql, picc, device):
    try:
        cur = mysql.connection.cursor()
        # ejecuta la consulta que guarda los datos en la BD
        cur.execute("INSERT INTO logs(PICC, device) VALUES (%s, %s)",(picc, str(device)))
        # persiste los cambio en la DB
        mysql.connection.commit()
        # cierra la coneccion con la DB
        cur.close()
        return 1
    except Exception as e:
        return 0



###--------------------------------------------------------------------------###
### Module test and develop ###
if __name__ == '__main__':
    pass
