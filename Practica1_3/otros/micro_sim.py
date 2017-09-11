import MySQLdb
from sys import exit
from time import sleep
from noise import pnoise1
from math import floor

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
    fnow = 999
    init_temp =  22
    init_hum = 65
    init_pres = 1010
    init_wind = 12

    temp = init_temp
    hum = init_hum
    pres = init_pres
    wind = init_wind

    cur = db.cursor()
    on = cur.execute("SELECT power FROM config WHERE power = 1")
    print 'on:', on

    while True:
        x = 0.0
        while on != 0:
            x += 0.01
            # -------------------------------
            result = cur.execute("SELECT MAX(freq) AS fMax, MIN(freq) AS fmin FROM config")
            if result > 0:
                r = cur.fetchone()
                fmax = r[0]
                fmin = r[1]
                print 'fmax:', fmax, 'fmin:', fmin

            temp += pnoise1(x, 1, 0.5, 2.0, 1024, 0)/10
            hum += pnoise1(x, 1, 0.5, 2.0, 1024, 256)/5
            pres += pnoise1(x, 1, 0.5, 2.0, 1024, 512)*10
            wind += pnoise1(x, 1, 0.5, 2.0, 1024, 768)*10
            fnow += fmin
            if fnow > fmax:
                fnow = fmin

            print 'temp:', '%.2f'%temp, 'hum:', floor(hum), 'pres:', floor(pres), 'wind:', floor(wind), 'freq:', fnow
            cur.execute("INSERT INTO samples(temp, hum, pres, wind, freq) VALUES(%s, %s, %s, %s, %s)", ('%.2f'%temp, floor(hum), floor(pres), floor(wind), fnow))
            sleep(fmin)
            # -------------------------------
            on = cur.execute("SELECT power FROM config WHERE power = 1")
            # cur.execute("UPDATE config SET power = 0")
            print 'on:', on

        print 'El microcontrolador fue apagado.'
        while on == 0:
            # -------------------------------
            print 'El micro se encuentra apagado...'
            sleep(10)
            # -------------------------------
            on = cur.execute("SELECT power FROM config WHERE power = 1")
            # cur.execute("UPDATE config SET power = 1")
            print 'on:', on

        print 'El microcontrolador fue encendido.'

    cur.close()

if __name__ == "__main__":
    main()
