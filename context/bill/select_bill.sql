SELECT id FROM bill
    WHERE id_user = {{ id_user }}
        ORDER BY date DESC;