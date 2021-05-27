-- Consulta en la tabla bill por el user_id, nos devuelve todo el historico de facturas arraigadas al user_id indicado.
SELECT id, id_user, date, total_quantity, total_price FROM bill
    WHERE bill.id_user = {{ id_user }}
        ORDER BY DATE DESC;