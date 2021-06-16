SELECT BILLDESCRIPTION.id_bill, CONCAT(PRODUCT.name, ' ', CONFIGURATION.name) product_name, BILLDESCRIPTION.quantity, BILLDESCRIPTION.price, BILL.date, Bill.status
FROM BILL
LEFT JOIN BILLDESCRIPTION
  ON BILLDESCRIPTION.id_bill = BILL.id
LEFT JOIN PRODUCT_CONFIGURATION
  ON PRODUCT_CONFIGURATION.id = BILLDESCRIPTION.id_product_config
LEFT JOIN PRODUCT
  ON PRODUCT.ID = PRODUCT_CONFIGURATION.product_id
LEFT JOIN CONFIGURATION
  ON CONFIGURATION.id = PRODUCT_CONFIGURATION.configuration_id
WHERE BILL.id_user = {{ id_user }}
ORDER BY BILL.date DESC;