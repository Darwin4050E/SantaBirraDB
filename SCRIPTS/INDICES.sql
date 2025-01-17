-- SANTABIRRADB
-- INDICES
USE SANTABIRRADB;

-- Índices de Product_Supplier:

CREATE INDEX IDX_COMPRAS_COMPOSITE
ON Product_Supplier(Bill_Date, Bill_Quantity);

CREATE INDEX IDX_PRODUCT_COMPOSITE
ON Product(Pro_Price);