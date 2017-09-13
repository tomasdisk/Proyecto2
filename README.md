# Proyecto2
Trabajos asociados a la materia Taller de Proyecto II

## Practica1_1
Contiene una aplicación que ejemplifica la utilización de Flask con un par de rutas y el procesamiento de información recibida por un formulario HTML. La información se procesa y persiste en una base de datos MySQL para poder ser solicitada y expuesta de la forma que se desee.

### Rutas:

  * __/__ : Es la página principal que contiene el formulario para completar y al mismo tiempo muestra la información almacenada en la BD. Muestra el listados de usuarios guardados y un porcentaje relativo a estos.
  * __/form__ : Es la ruta que se encarga de procesar el formulario y almacenarlo en la BD. Una vez echo esto redirige automáticamente a __/__.
  * __/develop__ : Página sin contenido.

### Base de Datos:
El archivo __BD.sql__ contiene todos las ordenes MySQL necesarias para crear y utilizar la BD con la aplicación Flask __app.py__.

La BD cuenta con una sola tabla _users_ que contiene la información que la app recibe de los formularios y con un usuario _flaskapp1_1_users_ con permisos específicos para la utilización de dicha tabla. Si ya existiera un usuario con ese nombre el script falla, por lo que previamente a correrlo habría que ejecutar el siguiente comando: `DROP USER 'flaskapp1_1_users'@'%';`.

El archivo __BD_5.7.sql__ es para versiones de MySQL 5.7 donde se resuelve el problema de que ya exista o no un usuario con el mismo nombre.

### Requerimientos:
Las librerías Python necesarias para ejecutar la app se encuentran en el archivo __requeriments.txt__.

### Ejecutar App:
Para poder poner en marcha la aplicación solo hay que descargar el repositorio y ejecutar los siguientes comandos:

  1. `pip install -r requeriments.txt`
  2. `mysql -u root -p < DB.sql` o `mysql -u root -p < DB_5.7.sql`
  3. `python app.py`

### Frameworks y otras librerías:
Los siguientes frameworks o librerías fueron necesarios para la realización de la app.

  * [Flask](https://github.com/pallets/flask).
  * [Flask-MySQLdb](https://github.com/admiralobvious/flask-mysqldb).
  * [Bootstrap](https://github.com/twbs/bootstrap).
  * [jQuery](https://github.com/jquery/jquery).


## Practica1_3
Contiene una aplicación que simula un microcontrolador (__micro_sim.py__) en la cual se generan periódicamente muestras de temperatura, presión, humedad y velocidad del viento para ser almacenadas en una BD. Por otra parte, una segunda aplicación (__app.py__) toma esas muestras, las procesa y las expone mediante interfaz web a medida que se van generando. Por los que el sistema completo simula la interacción entre una aplicación con servicios web y microcontrolador con acceso a la misma BD.

### Microcontrolador:
El archivo __micro_sim.py__ se encarga de simular el microcontrolador, generando las muestras cada una frecuencia fija de 5 segundos a partir de unos valores iniciales preseteados y la utilización de Perlin Noise para crear cambios pseudo aleatorios más realistas. Luego de guardar cada muestra en la BD el proceso se duerme los segundos necesarios hasta tener que generar la próxima.

### Rutas:

  * __/__ : Es la página principal en la que se muestran todos los datos generados por __micro_sim.py__ luego de ser adquiridos de la BD y procesados. La pagina se refresca automáticamente cada 5 segundos para exponer las nuevas muestras.
  * __/develop__ : Página sin contenido.

### Base de Datos:
El archivo __BD.sql__ contiene todos las ordenes MySQL necesarias para crear y utilizar la BD del sistema.

La BD cuenta con una sola tabla _samples_ donde __micro_sim.py__ guarda las muestras generadas para que __app.py__ las lea. Para una mejor administraron  de la BD cada aplicación tiene su propio usuario con los permisos necesarios para hacer uso de la tabla. Los usuarios son _flaskapp1_3_mic_ y _flaskapp1_3_app_ pero en el caso de que ya existieran usuarios con estos nombres el script fallaría, por lo que previamente a correrlo habría que ejecutar los siguiente comandos: `DROP USER 'flaskapp1_3_micro'@'%';` y `DROP USER 'flaskapp1_3_app'@'%';`.

El archivo __BD_5.7.sql__ es para versiones de MySQL 5.7 donde se resuelve el problema de que ya exista o no un usuario con el mismo nombre.

### Requerimientos:
Las librerías Python necesarias para ejecutar la app se encuentran en el archivo __requeriments.txt__.

### Ejecutar App:
Para poder poner en marcha la aplicación solo hay que descargar el repositorio y ejecutar los siguientes comandos:

  1. `pip install -r requeriments.txt`
  2. `mysql -u root -p < DB.sql` o `mysql -u root -p < DB_5.7.sql`
  3. `python micro_sim.py`
  4. `python app.py`

### Frameworks y otras librerías:
Los siguientes frameworks o librerías fueron necesarios para la realización de la app.

  * [Flask](https://github.com/pallets/flask).
  * [Flask-MySQLdb](https://github.com/admiralobvious/flask-mysqldb).
  * [MySQL-python](https://github.com/farcepest/MySQLdb1).
  * [Perlin Noise](https://github.com/caseman/noise).
  * [Bootstrap](https://github.com/twbs/bootstrap).
  * [jQuery](https://github.com/jquery/jquery).


## Practica1_4


### Microcontrolador:


### Rutas:

  * __/__ :

### Base de Datos:


### Requerimientos:
Las librerías Python necesarias para ejecutar la app se encuentran en el archivo __requeriments.txt__.

### Ejecutar App:
Para poder poner en marcha la aplicación solo hay que descargar el repositorio y ejecutar los siguientes comandos:

  1. `pip install -r requeriments.txt`
  2. `mysql -u root -p < DB.sql` o `mysql -u root -p < DB_5.7.sql`
  3. `python micro_sim.py`
  4. `python app.py`

### Frameworks y otras librerías:
Los siguientes frameworks o librerías fueron necesarios para la realización de la app.

  * [Flask](https://github.com/pallets/flask).
  * [Flask-MySQLdb](https://github.com/admiralobvious/flask-mysqldb).
  * [MySQL-python](https://github.com/farcepest/MySQLdb1).
  * [Perlin Noise](https://github.com/caseman/noise).
  * [Bootstrap](https://github.com/twbs/bootstrap).
  * [jQuery](https://github.com/jquery/jquery).
