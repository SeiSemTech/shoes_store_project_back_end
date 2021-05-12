-- Update columna product_id, configuration_id, config_display_order, sub_config_display_order, stock tabla product_configuration
--
UPDATE product_configuration 
    set product_id = {{product_id}}, configuration_id = {{configuration_id}}, 
    config_display_order = {{config_display_order}}, sub_config_display_order = {{sub_config_display_order}}, stock = {{stock}} 
        where id = {{id}};
