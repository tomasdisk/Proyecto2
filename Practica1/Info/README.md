## Info

### Cap1
Muestras las peticiones hechas por el navegador web al acceder a la url localhost:port/. Son todas peticiones GET para obtener los distintos recursos de la página. En el archivo __info.txt__ se muestran exactamente las mismas peticiones pero en la forma en que aparecen en la consola del servidor web.

### Cap2
Muestra el detalle de la primera petición GET donde se ven las cabeceras de dicha petición y de la respuesta que se obtuvo.

### Cap3
Muestra las transmisiones de paquetes a nivel TCP entre el servidor y el navegador web. Se puede ver perfectamente del paquete 1 al 22 cómo es que establecen la coneccion (paquetes __[SYN]__, __[SYN, ACK]__ y __[ACK]__), intercambian informacion (petición __GET / HTTP/1.1__ y respuesta __HTTP/1.0 200 OK (text/html)__) y luego finalizan la coneccion (paquetes __[FIN, ACK]__, __[FIN, ACK]__, __[ACK]__). También se puede apreciar que luego de que el navegador web recibe el recurso HTML solicita nuevas conecciones para pedir al servidor el resto de los recursos necesarios para desplegar la página web (css, js, imágenes, etc).

El archivo __cap3.pcapng__ contiene la captura de los paquetes de red descrita arriba.
