-- crea la BD sobrescribiendo la anterior en el caso de exixtir
DROP DATABASE IF EXISTS flaskapp1_3;
CREATE DATABASE flaskapp1_3;
USE flaskapp1_3;

-- crea la tabla samples que contiene los datos que genera el microcontrolador simulado
CREATE TABLE samples(id INT(11) AUTO_INCREMENT PRIMARY KEY, temp DECIMAL(5,2) NOT NULL, hum INT(2) NOT NULL, pres INT(4) NOT NULL, wind INT(3) NOT NULL, freq INT(2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- crea usuario para micro_sim con permisos especificos
CREATE USER 'flaskapp1_3_micro'@'%' IDENTIFIED BY 'flaskapp';
GRANT INSERT ON flaskapp1_3.samples TO 'flaskapp1_3_micro'@'%';

-- crea usuario para la app flask con permisos especificos
CREATE USER 'flaskapp1_3_app'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT ON flaskapp1_3.samples TO 'flaskapp1_3_app'@'%';
