SELECT users.user_id
FROM users
LEFT JOIN login
  ON users.user_id = login.user_id
WHERE users.email = {{email}}