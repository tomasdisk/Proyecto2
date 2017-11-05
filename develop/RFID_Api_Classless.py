from datetime import date


###--------------------------------------------------------------------------###
### Access to information ###

# Users

def RFID_getAllUsers():
    pass

def RFID_getUser(userId):
    pass

def RFID_getLastUser():
    pass

# Ids

def RFID_getAllPiccs():
    pass

def RFID_getPicc(piccId):
    pass

def RFID_getIdsByUser(user):
    pass

def RFID_getLastPicc():
    pass

# Devices

def RFID_getAllDevices():
    pass

def RFID_getDevice(deviceId):
    pass

# Logs

def RFID_getAllLogs():
    pass

def RFID_getLogsByUser(user):
    pass

def RFID_getLastLog():
    pass

def RFID_getLogsByDate(begin_date, end_date = date.min):
    pass

###--------------------------------------------------------------------------###
### Administation tools ###

# Users

def RFID_addUser(name, email, info_cod):
    pass

def RFID_delUser(user):
    pass

# Ids

def RFID_addId(user):
    pass

def RFID_delId(id):
    pass

# Devices

def RFID_addDevice(name, ip_adress, description):
    pass

def RFID_delDevice(device):
    pass

# Logs

def RFID_delLogsByUser(user):
    pass

def RFID_delLogsByDate(begin_date, end_date = date.min):
    pass

def RFID_delAllLogs():
    pass
