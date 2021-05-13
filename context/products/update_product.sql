-- Update columna name, image, price, description, category_id tabla product
--
UPDATE PRODUCT 
    set name = {{name}}, image = {{image}}, status = {{status}}, price = {{price}}, description = {{description}}, category_id = {{category_id}}, display_order = {{display_order}}
        where id = {{id}};