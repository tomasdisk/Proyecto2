import MySQLdb
from sys import exit
from time import sleep

try:
    db = MySQLdb.connect(
        host = 'localhost',
        user = 'flaskapp2_micro',
        passwd = 'flaskapp',
        db = 'flaskapp2'
    )
except Exception as e:
    sys.exit('No se pudo conectar a la BD')

def main():
    cur = db.cursor()
    on = cur.execute("SELECT power FROM config WHERE power = 1")
    print on

    while True:
        while on != 0:
            # -------------------------------
            print 'El micro se encuentra prendido...'
            sleep(2)


            # -------------------------------
            on = cur.execute("SELECT power FROM config WHERE power = 1")
            # cur.execute("UPDATE config SET power = 0")
            print on

        print 'El microcontrolador fue apagado.'
        while on == 0:
            # -------------------------------
            print 'El micro se encuentra apagado...'
            sleep(10)
            # -------------------------------
            on = cur.execute("SELECT power FROM config WHERE power = 1")
            # cur.execute("UPDATE config SET power = 1")
            print on

        print 'El microcontrolador fue encendido.'

    cur.close()

if __name__ == "__main__":
    main()
