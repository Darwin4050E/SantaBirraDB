-- SANTABIRRADB
-- REPORTES 
USE SANTABIRRADB;

-- View de reportar usando Product, Product_Supplier, Supplier.
CREATE VIEW VW_COMPRAS_GASTOSPROVEEDOR AS
SELECT Supplier.Sup_Ruc, Supplier.Sup_Name, SUM(Product_Supplier.Bill_Quantity * Product.Pro_Price) as Sup_Total
FROM Supplier
NATURAL JOIN Product_Supplier
NATURAL JOIN Product
GROUP BY Supplier.Sup_Ruc, Supplier.Sup_Name
ORDER BY Sup_Total DESC;