-- crea la BD sobrescribiendo la anterior en el caso de exixtir
-- DROP DATABASE IF EXISTS RFID_BD;
CREATE DATABASE RFID_BD;
USE RFID_BD;

--
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, PICC VARCHAR(20), description VARCHAR(200), count INT(2), registrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

--
CREATE TABLE logs(id INT(11) AUTO_INCREMENT PRIMARY KEY, PICC VARCHAR(20), device INT UNSIGNED, registrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

--
CREATE TABLE devs(id INT(11) AUTO_INCREMENT PRIMARY KEY, ipv4 INT UNSIGNED, description VARCHAR(20), registrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);


--
INSERT INTO users(PICC, description, count) VALUES
('2B044B2B', 'esta vaca es marron', 4),
('B19F2F34', 'esta vaca es muy rapida', 11);

INSERT INTO logs(PICC, device) VALUES
('2B044B2B', 1),
('B19F2F34', 2);

INSERT INTO devs(ipv4, description) VALUES
(1, "puerta 1"),
(2, "puerta 2");
