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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla rol
--

CREATE TABLE IF NOT EXISTS roles (
  role_id int(11) NOT NULL AUTO_INCREMENT,
  role_type varchar(30) NOT NULL,
  UNIQUE KEY (role_id)
);


-- --------------------------------------------------------

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
  UNIQUE KEY (user_id)
);

-- --------------------------------------------------------

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
  UNIQUE KEY (id)
);

CREATE TABLE IF NOT EXISTS configuration (
  id int(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(30) NOT NULL,
  sub_configuratuion VARCHAR(30) NOT NULL,
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

ALTER TABLE users
  ADD CONSTRAINT FK_USUARIO_ROL FOREIGN KEY (role_id) REFERENCES roles (role_id);

ALTER TABLE product
  ADD CONSTRAINT FK_CATEGORY FOREIGN KEY (category_id) REFERENCES category (id);

ALTER TABLE product_configuration
  ADD CONSTRAINT FK_PRODUCT FOREIGN KEY (product_id) REFERENCES product (id),
  ADD CONSTRAINT FK_CONFIGURATION FOREIGN KEY (configuration_id) REFERENCES configuration (id);

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

COMMIT;