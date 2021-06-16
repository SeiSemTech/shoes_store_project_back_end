SELECT
  Bill.id,
  BillDescription.id_product_config,
  CONCAT(PRODUCT.name, ' ', CONFIGURATION.name) name,
  BILL.date,
  BillDescription.quantity,
  BillDescription.price,
  Bill.status
FROM BillDescription
LEFT JOIN Bill
  ON BILL.id = BillDescription.id_bill
LEFT JOIN PRODUCT_CONFIGURATION
  ON PRODUCT_CONFIGURATION.id = BillDescription.id_product_config
LEFT JOIN PRODUCT
  ON PRODUCT.ID = PRODUCT_CONFIGURATION.product_id
LEFT JOIN CONFIGURATION
  ON CONFIGURATION.id = PRODUCT_CONFIGURATION.configuration_id