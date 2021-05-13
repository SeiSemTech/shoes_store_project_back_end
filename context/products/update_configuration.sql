-- Update columna name, sub_configuration, extra_price tabla configuration
--
UPDATE configuration 
    set name = {{name}}, sub_configuration = {{sub_configuration}}, extra_price = {{extra_price}}  
        where id = {{id}};