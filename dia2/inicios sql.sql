CREATE DATABASE prueba;
USE prueba;
CREATE TABLE clientes(
	# ahora definimos las columnas
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    dni CHAR(8) UNIQUE,
    carnet_extranjeria VARCHAR(10) UNIQUE,
    tipo_documento ENUM('C.E', 'DNI', 'RUC', 'PASAPORTE', 'C.M.', 'OTRO'),
    estado BOOL
); 