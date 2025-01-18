-- REPORTES SANTA BIRRA DB
USE SANTABIRRADB;

-- Reporte de ventas. 
-- Este reporte brinda información acerca de los productos más vendidos el último mes y las ganacias que han dejado a la discoteca 

CREATE VIEW VW_REPORTE_VENTAS_PRODUCTOS
AS 
SELECT 
p.Pro_Code, 
p.Pro_Name, 
p.Pro_UnitSize, 
cp.Cat_Name,
sum(ps.ProSale_Quantity) AS cantidadVendida, 
sum(ps.ProSale_Quantity) * p.Pro_SalePrice AS montoVendido,
(sum(ps.ProSale_Quantity) * p.Pro_SalePrice) - (sum(ps.ProSale_Quantity) * p.Pro_PurchasePrice) AS gananciasTotales
FROM SALE s
JOIN PRODUCT_SALE ps ON s.Sal_ID = ps.Sal_ID
JOIN PRODUCT p ON p.Pro_Code = ps.Pro_Code
JOIN CATEGORYPROD cp ON p.Cat_ID = cp.Cat_ID
WHERE s.Sal_Date > DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)
GROUP BY p.Pro_Code, p.Pro_Name, Pro_UnitSize, cp.Cat_Name
ORDER BY cantidadVendida DESC;

DROP VIEW VW_REPORTE_VENTAS_PRODUCTOS;
SELECT * FROM VW_REPORTE_VENTAS_PRODUCTOS;




