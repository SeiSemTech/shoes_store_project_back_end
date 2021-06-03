INSERT INTO Bill (id_user, date, total_quantity, total_price) VALUES
    ({{ id_user }}, CONVERT_TZ(UTC_TIMESTAMP(),'+00:00','-05:00'), {{ total_quantity }}, {{ total_price }});