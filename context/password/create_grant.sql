REPLACE INTO PASSWORD_GRANT (user_id, grant_key, expire_at) VALUES
  ({{ user_id }}, {{ grant_key }}, CONVERT_TZ(UTC_TIMESTAMP(),'+00:00','+01:00'));

