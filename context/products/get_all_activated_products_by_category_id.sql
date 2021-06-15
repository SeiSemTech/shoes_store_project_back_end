SELECT *
FROM product
WHERE status = 1
  AND category_id = {{ category_id }}
order by id desc