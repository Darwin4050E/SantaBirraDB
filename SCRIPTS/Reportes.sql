-- REPORTES SANTA BIRRA DB
USE SANTABIRRADB;

-- Reporte de ventas. 
-- Este reporte brinda información acerca de los productos más vendidos el último mes y las ganacias que han dejado a la discoteca 

CREATE VIEW VW_REPORTE_VENTAS_PRODUCTOS
AS 
SELECT 
p.Pro_Code AS codigoProducto, 
p.Pro_Name AS nombreProducto, 
p.Pro_UnitSize AS medida, 
cp.Cat_Name AS categoria,
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

-- Reporte de reservas. 
-- Este reporte brinda información acerca de las reservas completadas del ultimo año, eventos, asistentes y pagos.

CREATE VIEW VW_REPORTE_RESERVAS_COMPLETADAS
AS
SELECT rp.reserva_ID, rp.fecha, rp.hora, rp.evento, rp.asistentes,
rp.recaudacionHombres + rp.recaudacionMujeres AS totalRecaudacion, 
round(rp.descuentoPromocion * (rp.recaudacionHombres + rp.recaudacionMujeres),2) AS descuentoPromocion, 
round(rp.comisionPromotor * (rp.recaudacionHombres + rp.recaudacionMujeres),2) AS comisionPromotor,
round((rp.recaudacionHombres + rp.recaudacionMujeres) 
- ((rp.recaudacionHombres + rp.recaudacionMujeres) * (rp.descuentoPromocion + rp.comisionPromotor)), 2) AS montoAjustado,
COALESCE(rp.pagoRecibido,0) AS pagoRecibido

FROM
(
SELECT 
b.Boo_ID AS reserva_ID,
b.Boo_Date AS fecha,
b.Boo_Hour AS hora,
e.Eve_Name AS evento,
count(bc.Cus_ID) + 1 AS asistentes, -- Asistentes más la persona que realizó el evento
-- Subconsulta que calcula el total de asistentes hombres (verificando el que hizo la reserva) y lo multiplica por el precio para hombres.
((SELECT count(*) FROM CUSTOMER WHERE Cus_ID = b.Cus_ID AND Cus_Sex = 'M')
+ (SELECT count(Cus_ID) FROM BOOKING_CUSTOMER NATURAL JOIN CUSTOMER WHERE Cus_Sex = 'M' AND Boo_ID = b.Boo_ID)) 
* e.Eve_PMan AS recaudacionHombres,
-- Subconsulta que calcula el total de asistentes mujeres (verificando el que hizo la reserva) y lo multiplica por el precio para mujeres.
((SELECT count(*) FROM CUSTOMER WHERE Cus_ID = b.Cus_ID AND Cus_Sex = 'F')
+ (SELECT count(Cus_ID) FROM BOOKING_CUSTOMER NATURAL JOIN CUSTOMER WHERE Cus_Sex = 'F' AND Boo_ID = b.Boo_ID))
* e.Eve_PWoman  AS recaudacionMujeres,
-- Subconsulta que retorna la suma de los pagos hechos a esa reserva
(SELECT sum(Pay_Amount) FROM PAY WHERE Boo_ID = b.Boo_ID) AS pagoRecibido,

COALESCE(p.Prom_Descuento,0) AS descuentoPromocion,
COALESCE(pm.Prom_Com,0) AS comisionPromotor

FROM BOOKING b
JOIN EVENT e ON b.Eve_ID = e.Eve_ID
JOIN BOOKING_CUSTOMER bc ON b.Boo_ID = bc.Boo_ID
JOIN CUSTOMER c ON bc.Cus_ID = c.Cus_ID
LEFT JOIN PROMOTION p ON b.Prom_ID = p.Prom_ID
LEFT JOIN PROMOTOR pm ON b.Mem_ID = pm.Mem_ID
WHERE b.Sta_ID = (SELECT Sta_ID FROM STATUS WHERE Sta_Name = 'Completada') AND b.Boo_Date > DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
GROUP BY b.Boo_ID
) AS rp;

DROP VIEW VW_REPORTE_RESERVAS_COMPLETADAS;
SELECT * FROM VW_REPORTE_RESERVAS_COMPLETADAS;

-- REPORTE PARA CRUD DE PAGOS, INDICA EL MONTO REQUERIDO A PAGAR POR RESERVA.
CREATE VIEW VW_REPORTE_RESERVAS
AS
SELECT rp.reserva_ID,
rp.recaudacionHombres + rp.recaudacionMujeres AS totalRecaudacion, 
rp.descuentoPromocion, 
round((rp.recaudacionHombres + rp.recaudacionMujeres) 
- ((rp.recaudacionHombres + rp.recaudacionMujeres) * (rp.descuentoPromocion)), 2) AS ajusteRecaudacion,
COALESCE(rp.pagoRecibido,0) AS pagoRecibido

FROM
(
SELECT 
b.Boo_ID AS reserva_ID,
b.Boo_Date AS fecha,
b.Boo_Hour AS hora,
e.Eve_Name AS evento,
count(bc.Cus_ID) + 1 AS asistentes, -- Asistentes más la persona que realizó el evento
-- Subconsulta que calcula el total de asistentes hombres (verificando el que hizo la reserva) y lo multiplica por el precio para hombres.
((SELECT count(*) FROM CUSTOMER WHERE Cus_ID = b.Cus_ID AND Cus_Sex = 'M')
+ (SELECT count(Cus_ID) FROM BOOKING_CUSTOMER NATURAL JOIN CUSTOMER WHERE Cus_Sex = 'M' AND Boo_ID = b.Boo_ID)) 
* e.Eve_PMan AS recaudacionHombres,
-- Subconsulta que calcula el total de asistentes mujeres (verificando el que hizo la reserva) y lo multiplica por el precio para mujeres.
((SELECT count(*) FROM CUSTOMER WHERE Cus_ID = b.Cus_ID AND Cus_Sex = 'F')
+ (SELECT count(Cus_ID) FROM BOOKING_CUSTOMER NATURAL JOIN CUSTOMER WHERE Cus_Sex = 'F' AND Boo_ID = b.Boo_ID))
* e.Eve_PWoman  AS recaudacionMujeres,
-- Subconsulta que retorna la suma de los pagos hechos a esa reserva
(SELECT sum(Pay_Amount) FROM PAY WHERE Boo_ID = b.Boo_ID) AS pagoRecibido,

COALESCE(p.Prom_Descuento,0) AS descuentoPromocion,
COALESCE(pm.Prom_Com,0) AS comisionPromotor

FROM BOOKING b
JOIN EVENT e ON b.Eve_ID = e.Eve_ID
JOIN BOOKING_CUSTOMER bc ON b.Boo_ID = bc.Boo_ID
JOIN CUSTOMER c ON bc.Cus_ID = c.Cus_ID
LEFT JOIN PROMOTION p ON b.Prom_ID = p.Prom_ID
LEFT JOIN PROMOTOR pm ON b.Mem_ID = pm.Mem_ID
GROUP BY b.Boo_ID
ORDER BY b.Boo_ID
) AS rp;

SELECT * FROM VW_REPORTE_RESERVAS;

-- Reporte de Incidentes. 
-- Muestra los clientes que más incidentes registrados tienen en la discoteca.

CREATE VIEW VW_REPORTE_INCIDENTES_CLIENTE
AS
SELECT 
c.Cus_ID AS cedula, 
c.Cus_FName AS nombre, 
c.Cus_LName AS apellido, 
count(ic.IC_ID) AS numeroIncidentes, 
max(ic.Inc_Date) AS ultimoIncidente
FROM INCIDENT i
JOIN INCIDENT_CUSTOMER ic ON i.Inc_ID = ic.Inc_ID
JOIN CUSTOMER c ON c.Cus_ID = ic.Cus_ID
GROUP BY c.Cus_ID, c.Cus_FName, c.Cus_LName
HAVING numeroIncidentes > 1
ORDER BY numeroIncidentes DESC;

SELECT * FROM VW_REPORTE_INCIDENTES_CLIENTE;

-- Reporte de Inventarios. 
-- Muestra los productos que están próximos a quedarse sin existencias en la discoteca.

CREATE VIEW VW_REPORTE_MINIMAS_EXISTENCIAS
AS
SELECT 
p.Pro_Code AS codigo, 
P.Pro_Name AS producto, 
p.Pro_UnitSize AS medida, 
cp.Cat_Name AS categoria,
i.Inv_Stock AS existencias,
i.Inv_Date AS fechaUltimaActualizacion,
(SELECT Sup_RUC FROM SUPPLIER NATURAL JOIN PRODUCT_SUPPLIER WHERE Pro_Code = p.Pro_Code ORDER BY Bill_Date DESC LIMIT 1) AS rucProveedor,
(SELECT Sup_Name FROM SUPPLIER NATURAL JOIN PRODUCT_SUPPLIER WHERE Pro_Code = p.Pro_Code ORDER BY Bill_Date DESC LIMIT 1) AS proveedor

FROM PRODUCT p
JOIN CATEGORYPROD cp ON p.Cat_ID = cp.Cat_ID
JOIN INVENTORY i ON p.Pro_Code = i.Pro_Code 
WHERE i.Inv_ID = (SELECT Inv_ID FROM INVENTORY WHERE Pro_Code = p.Pro_Code ORDER BY Inv_ID DESC LIMIT 1)
HAVING existencias <= 25
ORDER BY existencias;

SELECT * FROM VW_REPORTE_MINIMAS_EXISTENCIAS;

-- Reporte de monto total de compras por proveedor.
-- View de reporte usando Product, Product_Supplier, Supplier.

CREATE VIEW V_COMPRAS_GASTOSPROVEEDOR AS
SELECT Supplier.Sup_Ruc, Supplier.Sup_Name, SUM(Product_Supplier.Bill_Quantity *  Pro_PurchasePrice) as Sup_Total
FROM Supplier
NATURAL JOIN Product_Supplier
NATURAL JOIN Product
GROUP BY Supplier.Sup_Ruc, Supplier.Sup_Name
ORDER BY Sup_Total DESC;

SELECT * FROM V_COMPRAS_GASTOSPROVEEDOR;

