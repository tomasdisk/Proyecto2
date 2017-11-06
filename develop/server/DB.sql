-- crea la BD sobrescribiendo la anterior en el caso de exixtir
DROP DATABASE IF EXISTS flaskapp1_4;
CREATE DATABASE flaskapp1_4;
USE flaskapp1_4;

-- crea la tabla config que contiene usuarios y sus parametros de configuracion (freq y power)
CREATE TABLE config(id INT(11) AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), power BOOLEAN, freq INT(2), updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

-- crea la tabla samples que contiene los datos que genera el microcontrolador simulado
CREATE TABLE samples(id INT(11) AUTO_INCREMENT PRIMARY KEY, temp DECIMAL(5,2) NOT NULL, hum INT(2) NOT NULL, pres INT(4) NOT NULL, wind INT(3) NOT NULL, freq INT(2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- crea usuario para micro_sim con permisos especificos
CREATE USER 'flaskapp1_4_mic'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT ON flaskapp1_4.config TO 'flaskapp1_4_mic'@'%';
GRANT INSERT ON flaskapp1_4.samples TO 'flaskapp1_4_mic'@'%';

-- crea usuario para la app flask con permisos especificos
CREATE USER 'flaskapp1_4_app'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT, INSERT, UPDATE, DELETE ON flaskapp1_4.config TO 'flaskapp1_4_app'@'%';
GRANT SELECT ON flaskapp1_4.samples TO 'flaskapp1_4_app'@'%';
