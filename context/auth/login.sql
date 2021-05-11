SELECT users.email, roles.role_type
FROM login
LEFT JOIN users
  ON users.user_id = login.user_id
LEFT JOIN roles
  ON roles.role_id = users.role_id
WHERE users.email = {{ email }}
  AND login.password = {{ password }};
