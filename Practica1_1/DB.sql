-- crea la BD sobrescribiendo la anterior en el caso de exixtir
DROP DATABASE IF EXISTS flaskapp1_1;
CREATE DATABASE flaskapp1_1;
USE flaskapp1_1;

-- crean la tabla users
CREATE TABLE users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), lastname VARCHAR(50), email VARCHAR(200), checked BOOLEAN, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- crea usuario dedicado con permisos especificos (SELECT, INSERT, DELETE) en tabla users
CREATE USER 'flaskapp1_1_user'@'%' IDENTIFIED BY 'flaskapp';
GRANT SELECT, INSERT, DELETE ON flaskapp1_1.users TO 'flaskapp1_1_user'@'%';

-- inserta 3 usuarios de ejemplo
INSERT INTO users(name, lastname, email, checked) VALUES
('juan', 'perex', 'perex@mail.com', 1),
('alto', 'rooller', 'rool@mail.com', 1),
('pepe', 'pepino', 'pepepino@mail.com', 0);

-- lista todos los usuarios
SELECT * FROM users;

-- busca el porcentaje de usuarios con checked = 1 (tildaron el checkbox)
SELECT (Count(id)* 100 / (SELECT COUNT(*) FROM users)) AS percent
FROM users
WHERE checked = 1;
