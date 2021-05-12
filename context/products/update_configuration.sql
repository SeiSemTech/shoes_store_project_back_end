-- Update columna name, sub_configuratuion, extra_price tabla configuration
--
UPDATE configuration 
    set name = {{name}}, sub_configuratuion = {{sub_configuratuion}}, extra_price = {{extra_price}}  
        where id = {{id}};