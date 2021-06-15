UPDATE bill
    SET total_quantity = {{ total_quantity }}, total_price = {{ total_price }}
    WHERE id = {{ id_bill }};