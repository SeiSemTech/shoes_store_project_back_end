-- Devuelve todos los registro de la tabla product_configuration que se encuentren con estado activo en la tabla product.
SELECT * FROM product_configuration
    WHERE product_id = {{product_id}};