DROP DATABASE IF EXISTS SANTABIRRADB;
CREATE DATABASE SANTABIRRADB;
USE SANTABIRRADB;

-- Tabla MEMBER
CREATE TABLE MEMBER (
    Mem_ID CHAR(10),
    Mem_FName VARCHAR(255) NOT NULL,
    Mem_LName VARCHAR(255) NOT NULL,
    Mem_Experience INT NOT NULL,
    CONSTRAINT PK_Member PRIMARY KEY (Mem_ID)
);

-- Tabla MANAGER
CREATE TABLE MANAGER (
    Mem_ID CHAR(10),
    CONSTRAINT PK_Manager PRIMARY KEY (Mem_ID),
    CONSTRAINT FK_Manager FOREIGN KEY (Mem_ID) REFERENCES MEMBER (Mem_ID) ON DELETE CASCADE 
);

-- Tabla PROMOTOR
CREATE TABLE PROMOTOR (
    Mem_ID CHAR(10),
    Mem_Man CHAR(10),
    Prom_Com DECIMAL(7,2) NOT NULL DEFAULT 0,
    CONSTRAINT PK_Promotor PRIMARY KEY (Mem_ID),
    CONSTRAINT FK_Promotor FOREIGN KEY (Mem_ID) REFERENCES MEMBER (Mem_ID) ON DELETE CASCADE,
    CONSTRAINT FK_PromMan FOREIGN KEY (Mem_Man) REFERENCES MANAGER (Mem_ID) ON DELETE SET NULL
);

-- Tabla GUARD
CREATE TABLE GUARD (
    Mem_ID CHAR(10),
    CONSTRAINT PK_Guard PRIMARY KEY (Mem_ID),
    CONSTRAINT FK_Guard FOREIGN KEY (Mem_ID) REFERENCES MEMBER (Mem_ID) ON DELETE CASCADE
);

-- Tabla SELLER
CREATE TABLE SELLER (
    Mem_ID CHAR(10),
    CONSTRAINT PK_Seller PRIMARY KEY (Mem_ID),
    CONSTRAINT FK_Seller FOREIGN KEY (Mem_ID) REFERENCES MEMBER (Mem_ID) ON DELETE CASCADE
);

-- Tabla CATEGORYPROD
CREATE TABLE CATEGORYPROD (
    Cat_ID INT AUTO_INCREMENT,
    Cat_Name VARCHAR(100) NOT NULL,
    CONSTRAINT PK_CategoryP PRIMARY KEY (Cat_ID)
);

-- Tabla PRODUCT
CREATE TABLE PRODUCT (
    Pro_Code INT AUTO_INCREMENT,
    Pro_Name VARCHAR(255) NOT NULL,
    Pro_Price DECIMAL(7,2) NOT NULL,
    Cat_ID INT NOT NULL,
    Pro_UnitSize VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Product PRIMARY KEY (Pro_Code),
    CONSTRAINT FK_ProductCat FOREIGN KEY (Cat_ID) REFERENCES CATEGORYPROD (Cat_ID) ON DELETE RESTRICT
);

-- Tabla SUPPLIER
CREATE TABLE SUPPLIER (
    Sup_RUC CHAR(13),
    Sup_Name VARCHAR(255) NOT NULL,
    Sup_Phone VARCHAR(255) NOT NULL,
    Sup_Email VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Supplier PRIMARY KEY (Sup_RUC)
);

-- Tabla PRODUCT_SUPPLIER
CREATE TABLE PRODUCT_SUPPLIER (
    Pro_Code INT,
    Sup_RUC CHAR(13),
    Bill_ID INT,
    Bill_Date DATE NOT NULL,
    Bill_Quantity INT NOT NULL CHECK (Bill_Quantity > 0),
    CONSTRAINT PK_Bill PRIMARY KEY (Pro_Code, Sup_RUC, Bill_ID),
    CONSTRAINT FK_BillProduct FOREIGN KEY (Pro_Code) REFERENCES PRODUCT (Pro_Code) ON DELETE RESTRICT,
    CONSTRAINT FK_BillSupplier FOREIGN KEY (Sup_RUC) REFERENCES SUPPLIER (Sup_RUC) ON DELETE RESTRICT
);

-- Tabla INVENTORY
CREATE TABLE INVENTORY (
    Inv_ID INT,
	Pro_Code INT,
    Inv_Date DATE NOT NULL,
    Inv_Stock INT NOT NULL CHECK (Inv_Stock >= 0),
    CONSTRAINT PK_Inventory PRIMARY KEY (Inv_ID, Pro_Code),
    CONSTRAINT FK_InventoryProduct FOREIGN KEY (Pro_Code) REFERENCES PRODUCT (Pro_Code) ON DELETE CASCADE
);

-- Tabla CUSTOMER
CREATE TABLE CUSTOMER (
    Cus_ID CHAR(10),
    Cus_FName VARCHAR(255) NOT NULL,
    Cus_LName VARCHAR(255) NOT NULL,
    Cus_Phone VARCHAR(255) NOT NULL,
    Cus_Email VARCHAR(255) NOT NULL,
    Cus_Sex CHAR(1) NOT NULL,
    CONSTRAINT PK_Customer PRIMARY KEY (Cus_ID)
);

-- Tabla SALE
CREATE TABLE SALE (
    Sal_ID INT,
    Sal_Date DATE NOT NULL,
    Mem_ID CHAR(10),
    Cus_ID CHAR(10) NOT NULL,
    CONSTRAINT PK_Sale PRIMARY KEY (Sal_ID),
    CONSTRAINT FK_SaleSeller FOREIGN KEY (Mem_ID) REFERENCES SELLER (Mem_ID) ON DELETE SET NULL,
    CONSTRAINT FK_SaleCustomer FOREIGN KEY (Cus_ID) REFERENCES CUSTOMER (Cus_ID) ON DELETE RESTRICT
);

-- Tabla Product_Sale
CREATE TABLE PRODUCT_SALE (
	Sal_ID INT,
    Pro_Code INT,
    ProSale_Quantity INT NOT NULL CHECK (ProSale_Quantity > 0),
    CONSTRAINT PK_ProductSale PRIMARY KEY (Sal_ID, Pro_Code),
    CONSTRAINT FK_ProductSale_SaleID FOREIGN KEY (Sal_ID) REFERENCES SALE (Sal_ID) ON DELETE CASCADE,
	CONSTRAINT FK_ProductSale_ProCode FOREIGN KEY (Pro_Code) REFERENCES PRODUCT (Pro_Code) ON DELETE RESTRICT
);

-- Tabla INCIDENT
CREATE TABLE INCIDENT (
    Inc_ID INT AUTO_INCREMENT,
    Inc_Desc VARCHAR(255) NOT NULL,
    Mem_ID CHAR(10),
    CONSTRAINT PK_Incident PRIMARY KEY (Inc_ID),
    CONSTRAINT FK_IncidentMem FOREIGN KEY (Mem_ID) REFERENCES MEMBER (Mem_ID) ON DELETE SET NULL
);

-- Tabla INCIDENT_CUSTOMER
CREATE TABLE INCIDENT_CUSTOMER (
	IC_ID INT,
    Inc_ID INT,
    Cus_ID CHAR(10),
    Inc_Date DATE NOT NULL,
    CONSTRAINT PK_IncCus PRIMARY KEY (IC_ID, Inc_ID, Cus_ID),
    CONSTRAINT FK_IncCusIncident FOREIGN KEY (Inc_ID) REFERENCES INCIDENT (Inc_ID) ON DELETE CASCADE,
    CONSTRAINT FK_IncCusCustomer FOREIGN KEY (Cus_ID) REFERENCES CUSTOMER (Cus_ID) ON DELETE CASCADE
);

-- Tabla CATEGORYEVE
CREATE TABLE CATEGORYEVE (
    Cat_ID INT AUTO_INCREMENT,
    Cat_Name VARCHAR(100) NOT NULL,
    CONSTRAINT PK_CategoryE PRIMARY KEY (Cat_ID)
);

-- Tabla EVENT
CREATE TABLE EVENT (
    Eve_ID INT AUTO_INCREMENT,
    Eve_Name VARCHAR(255) NOT NULL,
    Eve_PMan DECIMAL(7,2) NOT NULL CHECK (Eve_PMan >= 0),
    Eve_PWoman DECIMAL(7,2) NOT NULL CHECK (Eve_PWoman >= 0),
    Cat_ID INT NOT NULL,
    CONSTRAINT PK_Event PRIMARY KEY (Eve_ID),
    CONSTRAINT FK_EventCat FOREIGN KEY (Cat_ID) REFERENCES CATEGORYEVE (Cat_ID) ON DELETE RESTRICT
);

-- Tabla PROMOTION
CREATE TABLE PROMOTION (
    Prom_ID INT AUTO_INCREMENT,
    Prom_Name VARCHAR(255) NOT NULL,
    Prom_Descuento DECIMAL(7,2) NOT NULL CHECK (Prom_Descuento >= 0),
    CONSTRAINT PK_Promotion PRIMARY KEY (Prom_ID)
);

-- Tabla ZONE
CREATE TABLE ZONE (
    Zon_ID INT AUTO_INCREMENT,
    Zon_Capacity INT NOT NULL CHECK (Zon_Capacity >= 0),
    Mem_ID CHAR(10),
    Zon_Name VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Zone PRIMARY KEY (Zon_ID),
    CONSTRAINT FK_ZoneGuard FOREIGN KEY (Mem_ID) REFERENCES GUARD (Mem_ID) ON DELETE SET NULL
);

-- Tabla ZONEGENERAL
CREATE TABLE ZONEGENERAL (
    Zon_ID INT,
    CONSTRAINT PK_General PRIMARY KEY (Zon_ID),
    CONSTRAINT FK_GeneralZone FOREIGN KEY (Zon_ID) REFERENCES ZONE (Zon_ID) ON DELETE CASCADE
);

-- Tabla ZONEVIP
CREATE TABLE ZONEVIP (
    Zon_ID INT,
    Charge_VIP DECIMAL(7,2) NOT NULL CHECK (Charge_VIP >= 0),
    CONSTRAINT PK_VIP PRIMARY KEY (Zon_ID),
    CONSTRAINT FK_VIPZone FOREIGN KEY (Zon_ID) REFERENCES ZONE (Zon_ID) ON DELETE CASCADE
);

-- Tabla LOSTOBJECT
CREATE TABLE LOSTOBJECT (
    Los_ID INT AUTO_INCREMENT,
    Los_Date DATE NOT NULL,
    Los_Des VARCHAR(255) NOT NULL,
    Zon_ID INT,
    CONSTRAINT PK_LostObject PRIMARY KEY (Los_ID),
    CONSTRAINT FK_LostObjectZone FOREIGN KEY (Zon_ID) REFERENCES ZONE (Zon_ID) ON DELETE SET NULL
);

-- Tabla TABLES
CREATE TABLE TABLES (
    Tab_ID INT AUTO_INCREMENT,
    Zon_ID INT,
    CONSTRAINT PK_Tables PRIMARY KEY (Tab_ID),
    CONSTRAINT FK_TablesZone FOREIGN KEY (Zon_ID) REFERENCES ZONE (Zon_ID) ON DELETE CASCADE
);

-- Tabla STATUS
CREATE TABLE STATUS (
    Sta_ID INT AUTO_INCREMENT,
    Sta_Name VARCHAR(255) NOT NULL,
    CONSTRAINT PK_Status PRIMARY KEY (Sta_ID)
);

-- Tabla BOOKING
CREATE TABLE BOOKING (
    Boo_ID INT AUTO_INCREMENT,
    Boo_Date DATE NOT NULL,
    Boo_Hour TIME NOT NULL,
    Cus_ID CHAR(10) NOT NULL,
    Mem_ID CHAR(10),
    Prom_ID INT,
    Eve_ID INT NOT NULL,
    Sta_ID INT NOT NULL,
    CONSTRAINT PK_Booking PRIMARY KEY (Boo_ID),
    CONSTRAINT FK_BookingCustomer FOREIGN KEY (Cus_ID) REFERENCES CUSTOMER (Cus_ID) ON DELETE RESTRICT,
    CONSTRAINT FK_BookingPromotor FOREIGN KEY (Mem_ID) REFERENCES PROMOTOR (Mem_ID) ON DELETE SET NULL,
    CONSTRAINT FK_BookingPromotion FOREIGN KEY (Prom_ID) REFERENCES PROMOTION (Prom_ID) ON DELETE SET NULL,
    CONSTRAINT FK_BookingEvent FOREIGN KEY (Eve_ID) REFERENCES EVENT (Eve_ID) ON DELETE CASCADE,
    CONSTRAINT FK_BookingStatus FOREIGN KEY (Sta_ID) REFERENCES STATUS (Sta_ID) ON DELETE RESTRICT
);

-- Tabla BOOKING_ZONE
CREATE TABLE BOOKING_ZONE (
    Boo_ID INT,
    Zon_ID INT,
    CONSTRAINT PK_BookingZone PRIMARY KEY (Boo_ID, Zon_ID),
    CONSTRAINT FK_BookingZoneBooking FOREIGN KEY (Boo_ID) REFERENCES BOOKING (Boo_ID) ON DELETE CASCADE,
    CONSTRAINT FK_BookingZoneZone FOREIGN KEY (Zon_ID) REFERENCES ZONE (Zon_ID) ON DELETE CASCADE
);

-- Tabla BOOKING_CUSTOMER
CREATE TABLE BOOKING_CUSTOMER (
    Boo_ID INT,
    Cus_ID CHAR(10),
    CONSTRAINT PK_BookingCustomer PRIMARY KEY (Boo_ID, Cus_ID),
    CONSTRAINT FK_BookingCustomerBooking FOREIGN KEY (Boo_ID) REFERENCES BOOKING (Boo_ID) ON DELETE CASCADE,
    CONSTRAINT FK_BookingCustomerCustomer FOREIGN KEY (Cus_ID) REFERENCES CUSTOMER (Cus_ID) ON DELETE CASCADE
);

-- Tabla PAY
CREATE TABLE PAY (
	Pay_ID INT,
    Boo_ID INT,       
    Pay_Date DATE NOT NULL,    
    Pay_Amount DECIMAL(7, 2) NOT NULL CHECK (Pay_Amount >= 0),
    CONSTRAINT PK_Pay PRIMARY KEY (Pay_ID, Boo_ID), 
    CONSTRAINT FK_PayBooking FOREIGN KEY (Boo_ID) REFERENCES BOOKING (Boo_ID) ON DELETE CASCADE
);

-- DATOS 

-- Insertando todos los miembros base (20 empleados en total)
INSERT INTO MEMBER (Mem_ID, Mem_FName, Mem_LName, Mem_Experience) VALUES
-- Managers (5)
('0945678901', 'Carlos', 'Gómez', 5),
('0923456789', 'María', 'Velásquez', 6),
('0934567890', 'José', 'Zambrano', 7),
('0912345678', 'Andrea', 'Cevallos', 8),
('0956789012', 'Roberto', 'Mendoza', 6),

-- Promotores (5)
('0967890123', 'Ana', 'Pérez', 3),
('0978901234', 'Diana', 'Intriago', 2),
('0989012345', 'Martha', 'López', 4),
('0990123456', 'Karla', 'Macías', 3),
('0901234567', 'Patricia', 'Torres', 5),

-- Guardias (5)
('0913579246', 'Luis', 'Martínez', 4),
('0924680135', 'Jorge', 'Guerrero', 5),
('0935791357', 'Pedro', 'Montaño', 3),
('0946802468', 'Xavier', 'Castro', 6),
('0957913579', 'Diego', 'Ramírez', 4),

-- Vendedores (5)
('0968024680', 'Laura', 'Sánchez', 2),
('0979135791', 'Sofía', 'Jiménez', 3),
('0980246802', 'Paula', 'Núñez', 2),
('0991357913', 'Carmen', 'Morales', 4),
('0902468024', 'Daniela', 'Navarrete', 3);

-- Insertando Managers (5)
INSERT INTO MANAGER (Mem_ID) VALUES
('0945678901'),
('0923456789'),
('0934567890'),
('0912345678'),
('0956789012');

-- Insertando Promotores (5) con sus managers asignados
INSERT INTO PROMOTOR (Mem_ID, Mem_Man, Prom_Com) VALUES
('0967890123', '0945678901', 0.10),
('0978901234', '0923456789', 0.12),
('0989012345', '0934567890', 0.08),
('0990123456', '0912345678', 0.15),
('0901234567', '0956789012', 0.11);

-- Insertando Guardias (5)
INSERT INTO GUARD (Mem_ID) VALUES
('0913579246'),
('0924680135'),
('0935791357'),
('0946802468'),
('0957913579');

-- Insertando Vendedores (5)
INSERT INTO SELLER (Mem_ID) VALUES
('0968024680'),
('0979135791'),
('0980246802'),
('0991357913'),
('0902468024');

-- Insertando Zonas (Sólo dos zonas)
INSERT INTO ZONE (Zon_ID, Zon_Capacity, Mem_ID, Zon_Name) VALUES
(1, 50, '0913579246', 'VIP'),
(2, 100, '0924680135', 'General');

-- Insertando Zonas VIP y General
INSERT INTO ZONEGENERAL(Zon_ID) VALUES (2);

INSERT INTO ZONEVIP(Zon_ID, Charge_VIP)  VALUES (1, 10.00);

-- Tabla CATEGORYPROD (5 categorías de bebidas)
INSERT INTO CATEGORYPROD (Cat_Name) VALUES
('Cervezas Nacionales'),
('Cervezas Importadas'),
('Licores Fuertes'),
('Cocteles'),
('Bebidas Sin Alcohol');

-- Tabla PRODUCT (20 productos distribuidos en 5 categorías con unidades de medida)
INSERT INTO PRODUCT (Pro_Name, Pro_Price, Cat_ID, Pro_UnitSize) VALUES
-- Cervezas Nacionales (Cat_ID: 1)
('Pilsener', 4.00, 1, '330ml'),
('Club Premium', 4.50, 1, '330ml'),
('Club Negra', 5.00, 1, '330ml'),
('Pilsener Light', 4.00, 1, '330ml'),

-- Cervezas Importadas (Cat_ID: 2)
('Corona', 6.50, 2, '355ml'),
('Heineken', 7.00, 2, '330ml'),
('Stella Artois', 7.50, 2, '330ml'),
('Budweiser', 6.00, 2, '355ml'),

-- Licores Fuertes (Cat_ID: 3)
('Whisky Johnny Walker Shot', 15.00, 3, '45ml'),
('Ron Abuelo Shot', 12.00, 3, '45ml'),
('Vodka Absolut Shot', 13.00, 3, '45ml'),
('Tequila José Cuervo Shot', 14.00, 3, '45ml'),

-- Cocteles (Cat_ID: 4)
('Margarita', 8.50, 4, '250ml'),
('Mojito', 7.50, 4, '250ml'),
('Piña Colada', 8.00, 4, '250ml'),
('Cuba Libre', 7.00, 4, '250ml'),

-- Bebidas Sin Alcohol (Cat_ID: 5)
('Coca Cola', 3.00, 5, '400ml'),
('Agua Mineral', 2.50, 5, '500ml'),
('Red Bull', 5.00, 5, '250ml'),
('Sprite', 3.00, 5, '400ml');


-- Tabla SUPPLIER (20 proveedores ecuatorianos)
INSERT INTO SUPPLIER (Sup_RUC, Sup_Name, Sup_Phone, Sup_Email) VALUES
-- Proveedores de Cervezas Nacionales
('0992567841001', 'Cervecería Nacional CN S.A.', '043731800', 'ventas@cervecerianacional.ec'),
('0990023549001', 'Cervecería Zona Sur', '042970800', 'comercial@zonasur.ec'),
('0992156784001', 'Distribuidora Pílsener GYE', '043852147', 'ventas@pilsenergye.ec'),
('0991234567001', 'DINADEC S.A.', '042681900', 'pedidos@dinadec.ec'),

-- Proveedores de Cervezas Importadas
('0991567842001', 'Global Drinks Ecuador', '042456789', 'imports@globaldrinks.ec'),
('0992345678001', 'Premium Beers S.A.', '043456789', 'ventas@premiumbeers.com.ec'),
('0993456789001', 'Import Drinks GYE', '042567890', 'comercial@importdrinks.ec'),
('0994567890001', 'International Beverages', '043678901', 'ventas@intbeverages.ec'),

-- Proveedores de Licores Fuertes
('0995678902001', 'Corporación Azende', '042789012', 'ventas@azende.ec'),
('0996789019001', 'Juan El Juri', '043890123', 'comercial@eljuri.com.ec'),
('0997890123001', 'Distribuidora de Licores GYE', '042901234', 'ventas@licoresgye.ec'),
('0998901234001', 'ImportLicores Ecuador', '043012345', 'pedidos@importlicores.ec'),

-- Proveedores de Cocteles e Insumos
('0999012345001', 'Primeras Marcas Ecuador', '042123456', 'ventas@primerasmarcas.ec'),
('0990123456001', 'Mix Cocktails S.A.', '043234567', 'comercial@mixcocktails.ec'),
('0992234567001', 'Insumos de Bar Premium', '042345678', 'ventas@insumosbar.ec'),
('0992345679001', 'Bar Supplies Ecuador', '043456789', 'pedidos@barsupplies.ec'),

-- Proveedores de Bebidas Sin Alcohol
('0993456239001', 'The Coca-Cola Company Ecuador', '042567890', 'ventas@coca-cola.ec'),
('0994567891001', 'Tesalia Springs CBC', '043678901', 'comercial@tesalia.ec'),  
('0995678903001', 'Distribuidora de Gaseosas GYE', '042789012', 'ventas@gaseosasgye.ec'),
('0996789012001', 'Refrescos del Ecuador S.A.', '043890123', 'pedidos@refrescos.ec');


-- Tabla PRODUCT_SUPPLIER (una venta por cada proveedor)
INSERT INTO PRODUCT_SUPPLIER (Pro_Code, Sup_RUC, Bill_ID, Bill_Date, Bill_Quantity) VALUES
-- Proveedores de Cervezas Nacionales
(1, '0992567841001', 1, '2025-01-05', 500),  -- Pilsener con Cervecería Nacional
(2, '0990023549001', 2, '2025-01-05', 300),  -- Club Premium con Cervecería Zona Sur
(3, '0992156784001', 3, '2025-01-06', 250),  -- Club Negra con Distribuidora Pílsener
(4, '0991234567001', 4, '2025-01-06', 400),  -- Pilsener Light con DINADEC

-- Proveedores de Cervezas Importadas
(5, '0991567842001', 5, '2025-01-03', 200),  -- Corona con Global Drinks
(6, '0992345678001', 6, '2025-01-03', 150),  -- Heineken con Premium Beers
(7, '0993456789001', 7, '2025-01-03', 180),  -- Stella Artois con Import Drinks
(8, '0994567890001', 8, '2025-01-03', 220),  -- Budweiser con International Beverages

-- Proveedores de Licores Fuertes
(9, '0995678902001', 9, '2025-01-03', 50),   -- Whisky con Corporación Azende
(10, '0996789012001', 10, '2025-01-03', 40),  -- Ron con Juan El Juri
(11, '0997890123001', 11, '2025-01-03', 45),  -- Vodka con Distribuidora Licores
(12, '0998901234001', 12, '2025-01-03', 35),  -- Tequila con ImportLicores

-- Proveedores de Cocteles
(13, '0999012345001', 13, '2025-01-02', 100), -- Margarita con Primeras Marcas
(14, '0990123456001', 14, '2025-01-02', 120), -- Mojito con Mix Cocktails
(15, '0992234567001', 15, '2025-01-02', 90),  -- Piña Colada con Insumos Bar Premium
(16, '0992345678001', 16, '2025-01-02', 110), -- Cuba Libre con Bar Supplies

-- Proveedores de Bebidas Sin Alcohol
(17, '0993456789001', 17, '2025-01-02', 300), -- Coca Cola con The Coca-Cola Company Ecuador
(18, '0994567891001', 18, '2025-01-02', 200), -- Agua Mineral con Tesalia Springs CBC
(19, '0995678903001', 19, '2025-01-02', 250), -- Red Bull con Distribuidora de Gaseosas GYE
(20, '0996789012001', 20, '2025-01-02', 280); -- Sprite con Refrescos del Ecuador S.A.


-- Clientes
INSERT INTO CUSTOMER (Cus_ID, Cus_FName, Cus_LName, Cus_Phone, Cus_Email, Cus_Sex) VALUES
('0912345678', 'José', 'Pérez', '0991234567', 'jose.perez@gmail.com', 'M'),
('0912345679', 'Luis', 'Martínez', '0987654321', 'luis.martinez@gmail.com', 'M'),
('0912345680', 'Carlos', 'González', '0978765432', 'carlos.gonzalez@gmail.com', 'M'),
('0912345681', 'Juan', 'Ramírez', '0965432189', 'juan.ramirez@gmail.com', 'M'),
('0912345682', 'Jorge', 'Torres', '0956789123', 'jorge.torres@gmail.com', 'M'),
('0912345683', 'Ángel', 'Sánchez', '0943210987', 'angel.sanchez@gmail.com', 'M'),
('0912345684', 'Manuel', 'Cruz', '0932109876', 'manuel.cruz@gmail.com', 'M'),
('0912345685', 'Pedro', 'Moreno', '0921098765', 'pedro.moreno@gmail.com', 'M'),
('0912345686', 'Víctor', 'Alvarez', '0910987654', 'victor.alvarez@gmail.com', 'M'),
('0912345687', 'Santiago', 'Salazar', '0909876543', 'santiago.salazar@gmail.com', 'M'),

('0912345688', 'María', 'Rojas', '0992345678', 'maria.rojas@gmail.com', 'F'),
('0912345689', 'Rosa', 'Cordero', '0988765432', 'rosa.cordero@gmail.com','F'),
('0912345690', 'Ana', 'Díaz', '0975432109','ana.diaz@gmail.com','F'),
('0912345691','Carmen','Ponce','0964321098','carmen.ponce@gmail.com','F'),
('0912345692','Diana','Vásquez','0953210987','diana.vasquez@gmail.com','F'),
('0912345693','Blanca','Gómez','0942109876','blanca.gomez@gmail.com','F'),
('0912345694','Jessica','Aguirre','0931098765','jessica.aguirre@gmail.com','F'),
('0912345695','Andrea','Cano','0920987654','andrea.cano@gmail.com','F'),
('0912345696','Luz','Chávez','0919876543','luz.chavez@gmail.com','F'),
('0912345697','Sofía','Núñez','0908765432','sofia.nunez@gmail.com','F');


-- Tabla CategoryEve
INSERT INTO CATEGORYEVE (Cat_Name) VALUES
('Fiesta Temática'),
('Show en Vivo'),
('Deportivo'),
('Festividad de Temporada');

-- Tabla EVENT
INSERT INTO EVENT (Eve_Name, Eve_PMan, Eve_PWoman, Cat_ID) VALUES
('Fiesta Neon', 25.00, 12.00, 1),
('Fiesta de Disfraces Retro', 30.00, 15.00, 1),
('Fiesta de los 80s', 28.00, 14.00, 1),
('Fiesta de Máscaras', 27.00, 13.00, 1),
('Fiesta de Verano Tropical', 20.00, 10.00, 1),

('Concierto de Música Electrónica', 30.00, 15.00, 2),
('Noche de Jazz en Vivo', 25.00, 12.00, 2),
('Show de Comedia Stand-Up', 20.00, 10.00, 2),
('Noche de Rock Clásico', 26.00, 13.00, 2),

('Noche de Fútbol', 30.00, 15.00, 3),
('Torneo de Ecuavóley', 25.00, 12.00, 3),

('Halloween Party', 30.00, 15.00, 4),
('Navidad Electrónica', 25.00, 12.00, 4),
('Fiesta de Año Nuevo', 35.00, 18.00, 4),
('Carnaval Internacional', 28.00, 14.00, 4),
('Festival de Primavera', 22.00, 11.00, 4);

-- LOSTOBJECT (Objetos perdidos)
INSERT INTO LOSTOBJECT (Los_Date, Los_Des, Zon_ID) VALUES
('2024-12-05', 'Llaves de auto', 1),
('2024-12-06', 'Gorra blanca', 2),
('2024-12-07', 'Cámara fotográfica', 1),
('2024-12-12', 'Billetera de cuero', 2),
('2024-12-13', 'Paraguas rojo', 1),
('2024-12-14', 'Auriculares inalámbricos', 2),
('2024-12-19', 'Reloj de pulsera', 1),
('2024-12-20', 'Termo de agua azul', 2),
('2024-12-21', 'Cargador portátil', 1),
('2024-12-26', 'Libro de recetas', 2);

-- STATUS (Estados para las reservaciones)
INSERT INTO STATUS (Sta_Name) VALUES
('Pendiente'),
('Confirmada'),
('Cancelada'),
('Completada'),
('En Proceso');

INSERT INTO PROMOTION (Prom_Name, Prom_Descuento) VALUES
('Happy Hour', 0.15),       -- 15% de descuento en horarios específicos
('Cumpleañero', 0.50),      -- 50% de descuento para el cumpleañero
('Grupo +10', 0.20);        -- 20% de descuento para grupos de más de 10 personas


-- TABLES (Mesas en las zonas)
INSERT INTO TABLES (Zon_ID) VALUES
(1), -- Mesa 1 en zona VIP
(1), -- Mesa 2 en zona VIP
(1), -- Mesa 3 en zona VIP
(2), -- Mesa 4 en zona general
(2), -- Mesa 5 en zona general
(2), -- Mesa 6 en zona general
(2); -- Mesa 7 en zona general

-- INVENTORY (Control de stock)
INSERT INTO INVENTORY (Inv_ID, Pro_Code, Inv_Date, Inv_Stock) VALUES
-- Cervezas Nacionales
(1, 1, '2025-01-01', 100), -- Pilsener
(1, 2, '2025-01-01', 120), -- Club Premium
(1, 3, '2025-01-01', 80),  -- Club Negra
(1, 4, '2025-01-01', 90),  -- Pilsener Light

-- Cervezas Importadas
(1, 5, '2025-01-01', 60),  -- Corona
(1, 6, '2025-01-01', 70),  -- Heineken
(1, 7, '2025-01-01', 50),  -- Stella Artois
(1, 8, '2025-01-01', 65),  -- Budweiser

-- Licores Fuertes
(1, 9, '2025-01-01', 40),  -- Whisky Johnny Walker Shot
(1, 10, '2025-01-01', 50), -- Ron Abuelo Shot
(1, 11, '2025-01-01', 45), -- Vodka Absolut Shot
(1, 12, '2025-01-01', 55), -- Tequila José Cuervo Shot

-- Cocteles
(1, 13, '2025-01-01', 30), -- Margarita
(1, 14, '2025-01-01', 35), -- Mojito
(1, 15, '2025-01-01', 25), -- Piña Colada
(1, 16, '2025-01-01', 40), -- Cuba Libre

-- Bebidas Sin Alcohol
(1, 17, '2025-01-01', 200), -- Coca Cola
(1, 18, '2025-01-01', 180), -- Agua Mineral
(1, 19, '2025-01-01', 150), -- Red Bull
(1, 20, '2025-01-01', 190); -- Sprite


-- INCIDENT (Registro de incidentes)
INSERT INTO INCIDENT (Inc_Desc, Mem_ID) VALUES
('Cliente ebrio causando disturbios', '0913579246'),
('Robo reportado en la pista de baile', '0924680135'),
('Cliente atrapado en el baño', '0913579246'),
('Disputa por un área reservada', '0935791357'),
('Pelea entre dos grupos', '0957913579'),
('Cliente reporta tarjeta de crédito perdida', '0935791357'),
('Cliente descompensado por exceso de alcohol', '0924680135'),
('Incidente de ruido excesivo en el área VIP', '0957913579');

-- INCIDENT_CUSTOMER (Relación incidentes con clientes)
INSERT INTO INCIDENT_CUSTOMER (IC_ID, Inc_ID, Cus_ID, Inc_Date) VALUES
(1, 1, '0912345678', '2024-12-07'), -- Cliente ebrio causando disturbios
(1, 2, '0912345688', '2024-12-13'), -- Robo reportado en la pista de baile
(1, 2, '0912345685', '2024-12-13'), -- Robo reportado en la pista de baile (otro cliente implicado)
(1, 3, '0912345681', '2024-12-14'), -- Cliente atrapado en el baño
(1, 4, '0912345683', '2024-12-20'), -- Disputa por un área reservada
(1, 4, '0912345692', '2024-12-20'), -- Disputa por un área reservada (otro cliente implicado)
(1, 5, '0912345694', '2024-12-21'), -- Pelea entre dos grupos
(1, 5, '0912345686', '2024-12-21'), -- Pelea entre dos grupos (otro cliente implicado)
(1, 5, '0912345679', '2024-12-21'), -- Pelea entre dos grupos (otro cliente implicado)
(1, 6, '0912345697', '2024-12-26'), -- Cliente reporta tarjeta de crédito perdida
(1, 7, '0912345696', '2024-12-27'), -- Cliente descompensado por exceso de alcohol
(1, 8, '0912345693', '2024-12-28'), -- Incidente de ruido excesivo en el área VIP
(1, 8, '0912345691', '2024-12-28'), -- Incidente de ruido excesivo en el área VIP (otro cliente implicado)
(1, 8, '0912345687', '2024-12-28'); -- Incidente de ruido excesivo en el área VIP (otro cliente implicado)

-- BOOKING (Reservaciones)
-- Nuevas Reservaciones
INSERT INTO BOOKING (Boo_Date, Boo_Hour, Cus_ID, Mem_ID, Prom_ID, Eve_ID, Sta_ID) VALUES
('2024-12-05', '21:00:00', '0912345678', '0967890123', 1, 1, 3),
('2024-12-05', '22:00:00', '0912345679', '0978901234', 2, 2, 4),
('2024-12-06', '21:30:00', '0912345680', '0989012345', 3, 3, 3),
('2024-12-06', '23:00:00', '0912345681', '0990123456', 1, 4, 4),
('2024-12-07', '22:30:00', '0912345682', '0901234567', 2, 5, 3),
('2024-12-07', '23:00:00', '0912345683', '0967890123', 3, 6, 4),
('2024-12-12', '21:00:00', '0912345684', '0978901234', 1, 7, 3),
('2024-12-12', '22:00:00', '0912345685', '0989012345', 2, 8, 4),
('2024-12-13', '21:30:00', '0912345686', '0990123456', 3, 9, 3),
('2024-12-13', '23:00:00', '0912345687', '0901234567', 1, 10, 4),
('2024-12-14', '22:30:00', '0912345678', '0967890123', 2, 11, 3),
('2024-12-14', '23:00:00', '0912345679', '0978901234', 3, 12, 4),
('2024-12-19', '21:00:00', '0912345680', '0989012345', 1, 13, 3),
('2024-12-19', '22:00:00', '0912345681', '0990123456', 2, 14, 4),
('2024-12-20', '21:30:00', '0912345682', '0901234567', 3, 15, 3),
('2024-12-20', '23:00:00', '0912345683', '0967890123', 1, 16, 4),
('2024-12-21', '22:30:00', '0912345684', '0978901234', 2, 1, 3),
('2024-12-21', '23:00:00', '0912345685', '0989012345', 3, 2, 4),
('2024-12-26', '21:00:00', '0912345686', '0990123456', 1, 3, 3),
('2024-12-26', '22:00:00', '0912345687', '0901234567', 2, 4, 4);

-- BOOKING_ZONE (Relación reservas con zonas)
INSERT INTO BOOKING_ZONE (Boo_ID, Zon_ID) VALUES
(1, 1), -- Reserva en zona VIP
(2, 2), -- Reserva en zona general
(3, 2), -- Reserva en zona general
(4, 1), -- Reserva en zona VIP
(5, 2), -- Reserva en zona general
(6, 1), -- Reserva en zona VIP
(7, 1), -- Reserva en zona VIP
(8, 2), -- Reserva en zona general
(9, 2), -- Reserva en zona general
(10, 1), -- Reserva en zona VIP
(11, 1), -- Reserva en zona VIP
(12, 2), -- Reserva en zona general
(13, 1), -- Reserva en zona VIP
(14, 2), -- Reserva en zona general
(15, 1), -- Reserva en zona VIP
(16, 2), -- Reserva en zona general
(17, 1), -- Reserva en zona VIP
(18, 2), -- Reserva en zona general
(19, 1), -- Reserva en zona VIP
(20, 2); -- Reserva en zona general

-- Añadiendo dos clientes adicionales a cada reserva
INSERT INTO BOOKING_CUSTOMER (Boo_ID, Cus_ID) VALUES
(1, '0912345688'), (1, '0912345689'),
(2, '0912345690'), (2, '0912345691'),
(3, '0912345692'), (3, '0912345693'),
(4, '0912345694'), (4, '0912345695'),
(5, '0912345696'), (5, '0912345697'),
(6, '0912345688'), (6, '0912345689'),
(7, '0912345690'), (7, '0912345691'),
(8, '0912345692'), (8, '0912345693'),
(9, '0912345694'), (9, '0912345695'),
(10, '0912345696'), (10, '0912345697'),
(11, '0912345688'), (11, '0912345689'),
(12, '0912345690'), (12, '0912345691'),
(13, '0912345692'), (13, '0912345693'),
(14, '0912345694'), (14, '0912345695'),
(15, '0912345696'), (15, '0912345697'),
(16, '0912345688'), (16, '0912345689'),
(17, '0912345690'), (17, '0912345691'),
(18, '0912345692'), (18, '0912345693'),
(19, '0912345694'), (19, '0912345695'),
(20, '0912345696'), (20, '0912345697');

-- Pagos de las reservaciones
INSERT INTO PAY (Pay_ID, Boo_ID, Pay_Date, Pay_Amount) VALUES
(1, 1, '2024-12-05', 85.00),
(2, 2, '2024-12-05', 100.00),
(3, 3, '2024-12-06', 45.00),
(4, 4, '2024-12-06', 70.00),
(5, 5, '2024-12-07', 120.00),
(6, 6, '2024-12-07', 90.00),
(7, 7, '2024-12-12', 80.00),
(8, 8, '2024-12-12', 100.00),
(9, 9, '2024-12-13', 55.00),
(10, 10, '2024-12-13', 65.00),
(11, 11, '2024-12-14', 110.00),
(12, 12, '2024-12-14', 130.00),
(13, 13, '2024-12-19', 75.00),
(14, 14, '2024-12-19', 95.00),
(15, 15, '2024-12-20', 50.00),
(16, 16, '2024-12-20', 60.00),
(17, 17, '2024-12-21', 100.00),
(18, 18, '2024-12-21', 120.00),
(19, 19, '2024-12-26', 85.00),
(20, 20, '2024-12-26', 90.00);


-- Ventas de productos
INSERT INTO SALE (Sal_ID, Sal_Date, Mem_ID, Cus_ID) VALUES
(1,'2024-12-05', '0968024680', '0912345678'),
(2,'2024-12-05', '0979135791', '0912345679'),
(4,'2024-12-06', '0980246802', '0912345680'),
(5,'2024-12-06', '0991357913', '0912345681'),
(6,'2024-12-06', '0902468024', '0912345682'),
(7,'2024-12-07', '0968024680', '0912345683'),
(8,'2024-12-07', '0979135791', '0912345684'),
(9,'2024-12-07', '0980246802', '0912345685'),
(10,'2024-12-12', '0991357913', '0912345686'),
(11,'2024-12-12', '0902468024', '0912345687'),
(12,'2024-12-12', '0968024680', '0912345688'),
(13,'2024-12-13', '0979135791', '0912345689'),
(14,'2024-12-13', '0980246802', '0912345690'),
(15,'2024-12-13', '0991357913', '0912345691'),
(16,'2024-12-14', '0902468024', '0912345692'),
(17,'2024-12-14', '0968024680', '0912345693'),
(18,'2024-12-14', '0979135791', '0912345694'),
(19,'2024-12-19', '0980246802', '0912345695'),
(20,'2024-12-19', '0991357913', '0912345696'),
(21,'2024-12-19', '0902468024', '0912345697');

-- Ventas de productos con productos asignados
INSERT INTO PRODUCT_SALE (Sal_ID, Pro_Code, ProSale_Quantity) VALUES
(1, 1, 5), -- Pilsener 330ml
(1, 2, 4), -- Club Premium 330ml
(2, 5, 3), -- Corona 355ml
(2, 1, 3), -- Pilsener 330ml
(4, 7, 2), -- Stella Artois 330ml
(4, 9, 1), -- Piña Colada 250ml
(4, 1, 6), -- Pilsener 330ml
(4, 3, 3), -- Ron Abuelo Shot 45ml
(5, 6, 2), -- Heineken 330ml
(5, 4, 4), -- Budweiser 355ml
(6, 2, 5), -- Club Premium 330ml
(6, 5, 3), -- Corona 355ml
(7, 8, 4), -- Stella Artois 330ml
(7, 12, 2), -- Cuba Libre 250ml
(8, 9, 1), -- Piña Colada 250ml
(8, 13, 5), -- Sprite 400ml
(9, 10, 4), -- Vodka Absolut Shot 45ml
(9, 4, 3), -- Mojito 250ml
(10, 7, 3), -- Stella Artois 330ml
(10, 3, 5), -- Whisky Johnny Walker Shot 45ml
(11, 6, 5), -- Heineken 330ml
(11, 14, 2), -- Coca Cola 400ml
(12, 8, 3), -- Stella Artois 330ml
(12, 2, 4), -- Club Premium 330ml
(13, 9, 2), -- Piña Colada 250ml
(13, 1, 4), -- Pilsener 330ml
(14, 5, 3), -- Corona 355ml
(14, 12, 4), -- Cuba Libre 250ml
(15, 4, 5), -- Mojito 250ml
(15, 11, 2), -- Tequila José Cuervo Shot 45ml
(16, 14, 3), -- Coca Cola 400ml
(16, 6, 4), -- Heineken 330ml
(17, 3, 3), -- Ron Abuelo Shot 45ml
(17, 7, 2), -- Stella Artois 330ml
(18, 2, 4), -- Club Premium 330ml
(18, 8, 3), -- Stella Artois 330ml
(19, 10, 5), -- Vodka Absolut Shot 45ml
(19, 9, 1), -- Piña Colada 250ml
(20, 13, 4), -- Sprite 400ml
(20, 6, 2); -- Heineken 330ml

-- Triggers de Product_Supplier.

DELIMITER //
CREATE PROCEDURE SP_INVENTORY_RECUPERARID(
IN ProCode INT,
OUT InvId INT
)
BEGIN
	SELECT Inv_ID INTO InvId
    FROM Inventory
    WHERE Pro_Code = ProCode
    ORDER BY Inv_ID DESC 
    LIMIT 1;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER TRG_COMPRAS_AFTER_INSERT
AFTER INSERT ON Product_Supplier
FOR EACH ROW
BEGIN
    CALL SP_INVENTORY_RECUPERARID(NEW.Pro_Code, @InvId);
	UPDATE Inventory
    SET Inv_Stock = Inv_Stock + NEW.Bill_Quantity
    WHERE Inv_ID = @InvID AND Pro_Code = NEW.Pro_Code;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER TRG_COMPRAS_AFTER_UPDATE
AFTER UPDATE ON Product_Supplier
FOR EACH ROW
BEGIN
	CALL SP_INVENTORY_RECUPERARID(OLD.Pro_Code, @InvId);
	IF NEW.Bill_Quantity IS NOT NULL THEN
		UPDATE Inventory
		SET Inv_Stock = Inv_Stock + (NEW.Bill_Quantity - Inv_Stock)
		WHERE Inv_ID = @InvID AND Pro_Code = NEW.Pro_Code;
    ELSE
		UPDATE Inventory
		SET Inv_Date = NEW.Bill_Date
		WHERE Inv_ID = @InvID AND Pro_Code = NEW.Pro_Code;
	END IF;
END; //
DELIMITER ;

DELIMITER //
CREATE TRIGGER TRG_COMPRAS_AFTER_DELETE
AFTER DELETE ON Product_Supplier
FOR EACH ROW
BEGIN
    CALL SP_INVENTORY_RECUPERARID(OLD.Pro_Code, @InvId);
	UPDATE Inventory
    SET Inv_Stock = Inv_Stock - OLD.Bill_Quantity
    WHERE Inv_ID = @InvID AND Pro_Code = OLD.Pro_Code;
END; //
DELIMITER ;

-- View de reportar usando Product, Product_Supplier, Supplier.
CREATE VIEW VW_COMPRAS_GASTOSPROVEEDOR AS
SELECT Supplier.Sup_Ruc, Supplier.Sup_Name, SUM(Product_Supplier.Bill_Quantity * Product.Pro_Price) as Sup_Total
FROM Supplier
NATURAL JOIN Product_Supplier
NATURAL JOIN Product
GROUP BY Supplier.Sup_Ruc, Supplier.Sup_Name
ORDER BY Sup_Total DESC;

-- SP's de ProductSupplier:

DELIMITER //
CREATE PROCEDURE SP_COMPRAS_INSERTAR(
IN BillId INT, 
IN SupRuc CHAR(13), 
IN ProCode INT, 
IN BillDate DATE, 
IN BillQuantity INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La compra no pudo ser insertada.';
	END;
    START TRANSACTION;
		INSERT INTO Product_Supplier (Bill_ID, Sup_RUC, Pro_Code, Bill_Date, Bill_Quantity)
		VALUES (BillId, SupRuc, ProCode, BillDate, BillQuantity);
    COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_COMPRAS_CONSULTAR(
IN BillId INT, 
IN SupRuc CHAR(13), 
IN ProCode INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La compra no pudo ser consultada.';
    END;
    START TRANSACTION;
		SELECT Bill_Date, Bill_Quantity
		FROM Product_Supplier
		WHERE Bill_ID = BillId AND Sup_RUC = SupRuc AND Pro_Code = ProCode;
    COMMIT;
END; //
DELIMITER ;

-- SP para actualización de compras:

DELIMITER //
CREATE PROCEDURE SP_COMPRAS_ACTUALIZARFECHA(
IN BillId INT, 
IN SupRuc CHAR(13), 
IN ProCode INT, 
IN BillDate DATE
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La fecha de la compra no pudo ser actualizada.';
    END;
    START TRANSACTION;
		UPDATE Product_Supplier
		SET Bill_Date = BillDate
		WHERE Bill_ID = BillId AND Sup_RUC = SupRuc AND Pro_Code = ProCode;
    COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_COMPRAS_ACTUALIZARCANTIDAD(
IN BillId INT, 
IN SupRuc CHAR(13), 
IN ProCode INT, 
IN BillQuantity INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La cantidad de producto comprada no pudo ser actualizada.';
    END;
    START TRANSACTION;
		UPDATE Product_Supplier
		SET Bill_Quantity = BillQuantity
		WHERE Bill_ID = BillId AND Sup_Ruc = SupRuc AND Pro_Code = ProCode;
    COMMIT;
END; //
DELIMITER ;

-- SP para eliminación de compras.

DELIMITER //
CREATE PROCEDURE SP_COMPRAS_ELIMINAR(
IN BillId INT, 
IN SupRuc CHAR(13), 
IN ProCode INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La compra no pudo ser eliminada.';
    END;
    START TRANSACTION;
		DELETE FROM Product_Supplier
        WHERE Bill_ID = BillId AND Sup_RUC = SupRuc AND Pro_Code = ProCode;
    COMMIT;
END; //
DELIMITER ;

-- Índices de Product_Supplier:

CREATE INDEX IDX_COMPRAS_COMPOSITE
ON Product_Supplier(Bill_Date, Bill_Quantity);

CREATE INDEX IDX_PRODUCT_COMPOSITE
ON Product(Pro_Price);

-- Usuarios:

CREATE USER 'manager_user'@'%' IDENTIFIED BY 'ManPas001';

-- Permisos a usuarios:

GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_INSERTAR TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_CONSULTAR TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ACTUALIARFECHA TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ACTUALIZARCANTIDAD TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ELIMINAR TO 'manager_user'@'%';

GRANT EXECUTE ON SANTABIRRADB.VW_COMPRAS_GASTOSPROVEEDOR TO 'manager_user'@'%';