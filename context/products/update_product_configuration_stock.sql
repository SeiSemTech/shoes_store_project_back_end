-- Update columna stock, tabla product_configuration
--
UPDATE product_configuration 
    set stock = {{stock}} 
        where id = {{id}};
