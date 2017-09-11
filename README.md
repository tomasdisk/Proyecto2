# Proyecto2
Trabajos asociados a la materia Taller de Proyecto II

## Practica1_1
Contiene una aplicación que ejemplifica la utilización de Flask con un par de rutas y el procesamiento de información recibida por un formulario HTML. La información se procesa y persiste en una base de datos MySQL para poder ser solicitada y expuesta de la forma que se desee.

### Rutas:

  * __/__ : Es la página principal que contiene el formulario para completar y al mismo tiempo muestra la información almacenada en la BD. Muestra el listados de usuarios guardados y un porcentaje relativo a estos.
  * __/form__ : Es la ruta que se encarga de procesar el formulario y almacenarlo en la BD. Una vez echo esto redirige automáticamente a __/__.
  * __/develop__ : Página sin contenido.

### Base de Datos:
El achivo __BD.sql__ contiene todos las ordenes MySQL necesarias para crear y utilizar la BD con la aplicación Flask __app.py__.

La BD cuenta con una sola tabla _users_ que contiene la informacion que la app recibe de los formularios y con un usuario _flaskapp_users_ con permisos específicos para la utilización de dicha tabla. Si ya existiera un usuario con ese nombre el script falla, por lo que previamente a correrlo habría que ejecutar el siguiente comando: `DROP USER 'flaskapp_users'@'%';`.

El achivo __BD_5.7.sql__ es para versiones de MySQL 5.7 donde se resuelve el problema de que ya exista o no un usuario con el mismo nombre.

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
