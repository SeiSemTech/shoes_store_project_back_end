--Consulta la tabla Bill y trae el ID en orden descendiente por la fecha.
SELECT id FROM bill 
    WHERE id_user = {{ id_user }}
        ORDER BY date DESC;