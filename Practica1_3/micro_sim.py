import MySQLdb
from sys import exit
from time import sleep
from noise import pnoise1
from math import floor

try:
    db = MySQLdb.connect(
        host = 'localhost',
        user = 'flaskapp1_3_micro',
        passwd = 'flaskapp',
        db = 'flaskapp1_3'
    )
except Exception as e:
    sys.exit('No se pudo conectar a la BD')

def main():
    freq = 5
    init_temp =  22
    init_hum = 65
    init_pres = 1010
    init_wind = 12

    temp = init_temp
    hum = init_hum
    pres = init_pres
    wind = init_wind

    cur = db.cursor()

    x = 0.0
    while True:
        x += 0.01
        temp += pnoise1(x, 1, 0.5, 2.0, 1024, 0)/10
        hum += pnoise1(x, 1, 0.5, 2.0, 1024, 256)/5
        pres += pnoise1(x, 1, 0.5, 2.0, 1024, 512)*10
        wind += pnoise1(x, 1, 0.5, 2.0, 1024, 768)*10
        print 'temp:', '%.2f'%temp, 'hum:', floor(hum), 'pres:', floor(pres), 'wind:', floor(wind), 'freq:', freq
        cur.execute("INSERT INTO samples(temp, hum, pres, wind, freq) VALUES(%s, %s, %s, %s, %s)", ('%.2f'%temp, floor(hum), floor(pres), floor(wind), freq))
        db.commit()
        sleep(freq)

    cur.close()

if __name__ == "__main__":
    main()
