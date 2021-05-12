-- Update columnas display_order, name tabla category
--
UPDATE CATEGORY 
    set display_order = {{display_order}}, name = {{name}} 
        where id = {{id}};
