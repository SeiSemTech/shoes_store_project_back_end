--Realiza un update en el total quantity y el total price, para el id indicado.
UPDATE bill
    SET total_quantity = {{total_quantity}} AND total_price = {{total_price}}
    WHERE id_bill = {{id_bill}};