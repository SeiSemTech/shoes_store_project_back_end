--
-- Base de datos: zapacommerce
--

{% if prod %}
DROP DATABASE IF EXISTS zapacommerce;
CREATE DATABASE IF NOT EXISTS zapacommerce;
USE zapacommerce;
{% else %}
DROP DATABASE IF EXISTS zapacommercedev;
CREATE DATABASE IF NOT EXISTS zapacommercedev;
USE zapacommercedev;
{% endif %}



-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla login
--

CREATE TABLE IF NOT EXISTS login (
  user_id int(11) NOT NULL,
  password varchar(15) NOT NULL
);


CREATE TABLE IF NOT EXISTS password_grant (
  user_id int(11) NOT NULL,
  grant_key varchar(15) NOT NULL,
  expire_at timestamp NOT NULL,
  UNIQUE KEY (user_id)
);

--
-- Estructura de tabla para la tabla rol
--

CREATE TABLE IF NOT EXISTS roles (
  role_id int(11) NOT NULL AUTO_INCREMENT,
  role_type varchar(30) NOT NULL,
  UNIQUE KEY (role_id)
);


--
-- Estructura de tabla para la tabla users
--

CREATE TABLE IF NOT EXISTS users (
  user_id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(30) NOT NULL,
  email varchar(30) NOT NULL,
  phone varchar(30) NOT NULL,
  role_id int(11) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT False,
  UNIQUE KEY (user_id),
  UNIQUE KEY (email)
);

--
-- Estructura de tabla para productos
--


CREATE TABLE IF NOT EXISTS category (
  id int(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL,
  status int(2) NOT NULL,
  display_order int(2) NOT NULL,
  UNIQUE KEY (id)
);

CREATE TABLE IF NOT EXISTS product (
  id int(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL,
  status int(2) NOT NULL,
  image VARCHAR(30) NOT NULL,
  price int(11) NOT NULL,
  description VARCHAR(255) NOT NULL,
  category_id int(11) NOT NULL,
  display_order int(11) NOT NULL,
  UNIQUE KEY (id)
);

CREATE TABLE IF NOT EXISTS configuration (
  id int(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL,
  sub_configuration VARCHAR(30) NOT NULL,
  extra_price int(11),
  UNIQUE KEY (id)
);

CREATE TABLE IF NOT EXISTS product_configuration (
  id int(11) NOT NULL AUTO_INCREMENT,
  product_id int(11) NOT NULL,
  configuration_id int(11) NOT NULL,
  config_display_order int(11) NOT NULL,
  sub_config_display_order int(11) NOT NULL,
  stock int(11) NOT NULL,
  UNIQUE KEY (id)
);

--
-- Tablas Bill
--
CREATE TABLE IF NOT EXISTS BillDescription (
  id_bill int(11) NOT NULL AUTO_INCREMENT,
  id_product_config int(11) NOT NULL,
  product_name VARCHAR(30) NOT NULL,
  description VARCHAR(30) NOT NULL,
  quantity int(11) NOT NULL,
  price int(11) NOT NULL,
  total int(11) NOT NULL,
  UNIQUE KEY (id_bill)
);

CREATE TABLE IF NOT EXISTS bill (
  id int(11) NOT NULL,
  id_user int(11) NOT NULL,
  date timestamp NOT NULL,
  total_quantity int(11) NOT NULL,
  total_price int(11) NOT NULL,
  UNIQUE KEY (id)
);
--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla login
--
ALTER TABLE login
  ADD PRIMARY KEY (user_id);

--
-- Indices de la tabla rol
--
ALTER TABLE roles
  ADD PRIMARY KEY (role_id);

--
-- Indices de la tabla users
--
ALTER TABLE users
  ADD PRIMARY KEY (user_id),
  ADD KEY FK_USUARIO_ROL (role_id);

ALTER TABLE category
  ADD PRIMARY KEY (id);

ALTER TABLE product
  ADD PRIMARY KEY (id),
  ADD KEY FK_CATEGORY (category_id);

ALTER TABLE configuration
  ADD PRIMARY KEY (id);

ALTER TABLE product_configuration
  ADD PRIMARY KEY (id),
  ADD KEY FK_PRODUCT (product_id),
  ADD KEY FK_CONFIGURATION (configuration_id);


--
-- Restricciones para tablas volcadas
--

ALTER TABLE login
  ADD CONSTRAINT FK_LOGIN_USUARIO FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE password_grant
  ADD CONSTRAINT FK_USER_ID FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE users
  ADD CONSTRAINT FK_USUARIO_ROL FOREIGN KEY (role_id) REFERENCES roles (role_id);

ALTER TABLE product
  ADD CONSTRAINT FK_CATEGORY FOREIGN KEY (category_id) REFERENCES category (id);

ALTER TABLE product_configuration
  ADD CONSTRAINT FK_PRODUCT FOREIGN KEY (product_id) REFERENCES product (id),
  ADD CONSTRAINT FK_CONFIGURATION FOREIGN KEY (configuration_id) REFERENCES configuration (id);

ALTER TABLE BillDescription
  ADD CONSTRAINT FK_BILLDESCRIPTION_PRODUCT_CONFIGURATION FOREIGN KEY (id_product_config) REFERENCES product_configuration (id),
  ADD CONSTRAINT FK_BILLDESCRIPTION_BILL FOREIGN KEY (id_bill) REFERENCES bill (id);

ALTER TABLE Bill
  ADD CONSTRAINT FK_BILL_USERS FOREIGN KEY (id_user) REFERENCES USERS (user_id);
--
-- Poblar base de datos
--
INSERT INTO roles (role_type) VALUES
  ('Administrador'),
  ('Usuario Registrado'),
  ('Usuario Anonimo');

INSERT INTO users (name, email, phone, role_id) VALUES
  ('Admin', 'admin@zapacommerce.com', '3123026202', 1),
  ('User', 'user@zapacommerce.com', '3123026203', 2);

INSERT INTO login (user_id, password) VALUES
  (1, 'admin'),
  (2, 'user');

INSERT INTO category (name, status, display_order) VALUES
  ('Promociones', 1, 1),
  ('Temporada de Verano', 0, 2);

INSERT INTO product (name, status, image, price, description, category_id, display_order) VALUES
  ('Zapatillas Nike', 1, 'Url Imagen', 150000, 'Hermosa Zapatilla Nike con tecnologia de Running', 1, 1),
  ('Zapatillas Adidas', 1, 'Url Imagen', 220000, 'Hermosa Zapatilla Adidas con tecnologia ultraboost', 1, 2),
  ('Zapatillas Puma', 0, 'Url Imagen', 280000, 'Hermosa Zapatilla Puma para salto', 2, 3);

INSERT INTO configuration (name, sub_configuration, extra_price) VALUES
  ('Talla', 38, 0),
  ('Talla', 39, 10000),
  ('Talla', 40, 10000),
  ('Talla', 41, 12000),
  ('Color', 'Azul', 5000),
  ('Color', 'Blanco', 0),
  ('Color', 'Negro', 0),
  ('Color', 'Rojo', 5000),
  ('Color', 'Verde', 5000);

INSERT INTO product_configuration (product_id, configuration_id, config_display_order, sub_config_display_order, stock) VALUES
 -- Producto 1
 (1, 1, 1, 1, 5),
 (1, 2, 1, 2, 5),
 (1, 3, 1, 3, 5),
 (1, 4, 1, 4, 5),
 (1, 5, 2, 1, 5),
 (1, 6, 2, 2, 5),
 (1, 7, 2, 3, 5),
 (1, 8, 2, 4, 5),
 -- Producto 2
 (2, 1, 1, 1, 5),
 (2, 2, 1, 2, 5),
 (2, 3, 1, 3, 5),
 (2, 4, 1, 4, 5),
 (2, 5, 2, 1, 5),
 (2, 6, 2, 2, 5),
 (2, 7, 2, 3, 5),
 (2, 8, 2, 4, 5),
 -- Producto 3
 (3, 1, 1, 1, 5),
 (3, 2, 1, 2, 5),
 (3, 3, 1, 3, 5),
 (3, 4, 1, 4, 5),
 (3, 5, 2, 1, 5),
 (3, 6, 2, 2, 5),
 (3, 7, 2, 3, 5),
 (3, 8, 2, 4, 5);

COMMIT;