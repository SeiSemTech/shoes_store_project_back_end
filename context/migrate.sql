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

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla login
--
ALTER TABLE login
  ADD CONSTRAINT FK_LOGIN_USUARIO FOREIGN KEY (user_id) REFERENCES users (user_id);

--
-- Filtros para la tabla users
--
ALTER TABLE users
  ADD CONSTRAINT FK_USUARIO_ROL FOREIGN KEY (role_id) REFERENCES roles (role_id);

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