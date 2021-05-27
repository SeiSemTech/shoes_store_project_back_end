SELECT product_configuration.id,
       configuration.name,
       configuration.sub_configuration,
       configuration.extra_price,
       product_configuration.config_display_order,
       product_configuration.sub_config_display_order,
       product_configuration.stock
FROM product_configuration
LEFT JOIN configuration
  ON configuration.id = product_configuration.configuration_id
WHERE product_id = {{product_id}};