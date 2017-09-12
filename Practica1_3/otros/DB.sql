-- crea la BD sobrescribiendo la anterior en el caso de exixtir
DROP DATABASE IF EXISTS flaskapp2;
CREATE DATABASE flaskapp2;
USE flaskapp2;

-- crea la tabla config que contiene usuarios y sus parametros de configuracion (freq y power)
CREATE TABLE config(id INT(11) AUTO_INCREMENT PRIMARY KEY, user VARCHAR(50), power BOOLEAN, freq INT(2), updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

-- crea la tabla samples que contiene los datos que genera el microcontrolador simulado
CREATE TABLE samples(id INT(11) AUTO_INCREMENT PRIMARY KEY, temp DECIMAL(5,2) NOT NULL, hum INT(2) NOT NULL, pres INT(4) NOT NULL, wind INT(3) NOT NULL, freq INT(2), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- crea usuario para micro_sim con permisos especificos
-- DROP USER IF EXISTS 'flaskapp2_micro'@'%';
CREATE USER 'flaskapp2_micro'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT ON flaskapp2.config TO 'flaskapp2_micro'@'%';
GRANT INSERT ON flaskapp2.samples TO 'flaskapp2_micro'@'%';

-- crea usuario para la app flask con permisos especificos
-- DROP USER IF EXISTS 'flaskapp2_app'@'%';
CREATE USER 'flaskapp2_app'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT, INSERT, UPDATE, DELETE ON flaskapp2.config TO 'flaskapp2_app'@'%';
GRANT SELECT ON flaskapp2.samples TO 'flaskapp2_app'@'%';

-- inserta un usuarios de ejemplo
INSERT INTO config(user, power, freq) VALUES
('admin', 1, 40);

-- lista al usuario insertado
SELECT * FROM config c WHERE c.user = 'admin';
