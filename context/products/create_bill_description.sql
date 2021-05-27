-- Se inserta un registro en la tabla BillDescription
INSERT INTO BillDescription (id_bill, id_product_config, product_name, description, quantity, price, total) VALUES
    ({{ id_bill }}, {{ id_product_config }}, {{ product_name }}, {{ description }}, {{ quantity }}, {{ price }}, {{ total }});