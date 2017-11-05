

class RFIDUser():

    def __init__(self, name, DNI, email):

        self.name = name
        self.DNI = DNI
        self.email = email

    def getIds(self):
        pass

    def delId(self, RFIDId):
        pass

    @staticmethod
    def delUser(RFIDUser):
        pass


class RFIDId():

    def __init__(self, RFIDUser, rfid):

        self.user = RFIDUser
        self.id = rfid

class
