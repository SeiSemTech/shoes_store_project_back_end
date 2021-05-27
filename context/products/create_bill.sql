-- Se inserta un registro en la tabla Bill, en pocas palabras crea una factura
INSERT INTO Bill (id, id_user, date, total_quantity, total_price) VALUES
    ({{ id }}, {{ id_user }}, {{ date }}, {{ total_quantity }}, {{ total_price }});