-- Update columna name, image, price, description, category_id tabla product
--
UPDATE PRODUCT 
    set name = {{name}}, image = {{image}}, price = {{price}}, description = {{description}}, category_id = {{category_id}} 
        where id = {{id}};