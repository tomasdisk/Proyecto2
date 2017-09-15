## Practica1_4
Es una mejora de las aplicaciones de la Practica1_3 donde se le da al usuario la posibilidad de cambiar la frecuancia de muestreo del microcontrolador como tambien de apagarlo. Al mismo tiempo se admiten multiples usuarios con distintas frecuancias y la posibilidad de estar logueado o no. Para esto se necesita que el microcontrolador (__micro_sim.py__) sepa manejar los posibles inconvenientes que se peudan generar y que el servidor web (__app.py__) haga un manejo de los usuarios registrados. El sistema completo continua simulando la interacción entre una aplicación con servicios web y un microcontrolador con acceso a la misma BD.


### Microcontrolador:
El archivo __micro_sim.py__ se encarga de simular el microcontrolador, generando las muestras a partir de unos valores iniciales preseteados y la utilización de Perlin Noise para crear cambios pseudo aleatorios más realistas. La cantida de muestras por segundo que se genera varia entre los valores 1, 5, 10, 20 y 40. Como este valor es elegido por los usuarios, el microcontrolador busca en la BD entre los datos de los usuarios y como necesita satisfacer las peticiones de todos, genera las muestras a la mayor velocidad solicitada. Luego de guardar cada muestra en la BD el proceso se duerme los segundos necesarios hasta tener que generar la próxima.

El microcontrolador tambien cuanta con la posibilidad de estar apagado, ya sea porque todos los usuarios decidieron apagarlo o porque no hay ninguno logueado. Mientras un usuario lo mantenga encendido el microcontrolador va a seguir generando las muestras.

### Rutas:

  * __/__ : Es la página principal donde el usuario puede hacer login o logout, contiene los formularios para que el usuario logueado encienda y apague el micro, como para que elija la frecuencia de muestreo. Tambien expone al usuario las ultimas muestras realizadas por el microcontrolador, actualizandolas mediante AJAX cada la frecuencia elegida. Hay que aclarar que si varios usuarios registrados tiene seteadas distintas frecuencias, cada uno ve las muestras de la frecuencia que elegió. Si el usuario __A__ eligió 1 muetra por segundo y el __B__ una cada 5 segundos, el __A__ va a ver las muestras 1, 2, 3, 4, 5, 6, 7, 8, 9 y 10 mientras que el __B__ sólo las 5 y 10.
  * __/refreshData__ : Esta ruta se usa para solicitar los datos de las ultimas muestras al servidor. Funciona como una API, recibe una solicitud GET, busca la informacion en la BD y la devuelve en formato JSON al usuario.
  * __/form_power__ : Recibe las solicitudes del usuario de encender o apagar el microcontrolador. Esta informacion se guarda en la BD con los datos del usuario para que el microcontrolador pueda hacer uso de ella.
  * __/form_sense/<freq>__ : Se encanrga de procesar el formulario en el que un usuario solicita cambiar su frecuencia de muestreo. Dicha frecuencia es actualizada en la BD junto con los datos de ese usuario.
  * __/develop__ : Página sin contenido.
  * __/login__ : Es la ruta a traves de la cual el usuario se loguea y se le crea automaticamente un usuario para la session actual con un nombre y frecuencia de muestreo fijas. Luego se persiste esta informacion en la BD para que el microcontrolador pueda hacer uso de ella y se redirecciona a __/__.
  * __/logout__ : En esta ruta se elimina el usuario actual tanto de la session com de la BD y se redirecciona hacia __/__ a la espera de un nuevo logueo.

### Base de Datos:
El archivo __BD.sql__ contiene todos las ordenes MySQL necesarias para crear y utilizar la BD del sistema.

La BD cuenta con dos tablas _samples_ donde __micro_sim.py__ guarda las muestras generadas para que __app.py__ las lea y _config_ donde se almacenan los usuarios y su informacion de control sobre el microcontrolador. Para una mejor administraron  de la BD cada aplicación tiene su propio usuario con los permisos necesarios para hacer uso de las tablas. Los usuarios son _flaskapp1_3_mic_ y _flaskapp1_3_app_ pero en el caso de que ya existieran usuarios con estos nombres el script fallaría, por lo que previamente a correrlo habría que ejecutar los siguiente comandos: `DROP USER 'flaskapp1_3_micro'@'%';` y `DROP USER 'flaskapp1_3_app'@'%';`.

El archivo __BD_5.7.sql__ es para versiones de MySQL 5.7 donde se resuelve el problema de que ya exista o no un usuario con el mismo nombre.

### Requerimientos:
Las librerías Python necesarias para ejecutar la app se encuentran en el archivo __requeriments.txt__.

### Ejecutar App:
Para poder poner en marcha la aplicación solo hay que descargar el repositorio y ejecutar los siguientes comandos:

  1. `pip install -r requeriments.txt`
  2. `mysql -u root -p < DB.sql` o `mysql -u root -p < DB_5.7.sql`
  3. `python micro_sim.py`
  4. `python app.py`

Luego en un navegador web ir a la url `localhost:8002`.

### Frameworks y otras librerías:
Los siguientes frameworks o librerías fueron necesarios para la realización de la app.

  * [Flask](https://github.com/pallets/flask).
  * [Flask-MySQLdb](https://github.com/admiralobvious/flask-mysqldb).
  * [MySQL-python](https://github.com/farcepest/MySQLdb1).
  * [Perlin Noise](https://github.com/caseman/noise).
  * [Bootstrap](https://github.com/twbs/bootstrap).
  * [jQuery](https://github.com/jquery/jquery).
