-- SANTABIRRADB
-- STORED PROCEDURES
USE SANTABIRRADB;

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

-- SP's de Inventory
-- SP para obtener el último ID artificial del inventario de un producto.

DELIMITER //
CREATE PROCEDURE SP_ULTIMO_ID_INVENTARIO(
IN codigoProducto INT, 
OUT idInventario INT)
BEGIN
	DECLARE ultimoInventario INT DEFAULT 0;
    SET ultimoInventario = (SELECT Inv_ID 
    FROM INVENTORY 
    WHERE Pro_Code = codigoProducto 
    ORDER BY Inv_ID DESC LIMIT 1);
    
    IF ultimoInventario IS NULL THEN
		SET ultimoInventario = 0;
	END IF;
    
    SET idInventario = ultimoInventario + 1;
END //
DELIMITER ;

-- SP para insertar inventario (Cuando se realiza conteo manual)
-- Las existencias se actualizan automáticamente cuando se realiza una compra o una venta.

DELIMITER //
CREATE PROCEDURE SP_INSERTAR_INVENTORY(IN codigoProducto INT, 
IN fecha DATE, 
IN stock INT)
BEGIN
	DECLARE ultimoInventario INT DEFAULT 1;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No se pudo agregar el inventario. Verifique e intente de nuevo.';
    END;

	START TRANSACTION;

    CALL SP_ULTIMO_ID_INVENTARIO(codigoProducto, @idInventario);
    SET ultimoInventario = (SELECT @idInventario);
    
	INSERT INTO INVENTORY (Inv_ID, Pro_Code, Inv_Date, Inv_Stock) 
    VALUES (ultimoInventario, codigoProducto, fecha, stock);
    
    COMMIT;
END //
DELIMITER ;

-- SP para obtener el último ID del inventario de un producto POR FECHA.

DELIMITER //
CREATE PROCEDURE SP_ULTIMO_ID_INVENTARIO_FECHA(
IN codigoProducto INT, 
OUT idInventario INT)
BEGIN
	DECLARE ultimoInventario INT DEFAULT 0;
    SET ultimoInventario = (SELECT Inv_ID 
    FROM INVENTORY WHERE Pro_Code = codigoProducto 
    ORDER BY Inv_Date DESC LIMIT 1);
    
    IF ultimoInventario IS NULL THEN
		SET ultimoInventario = 0;
	END IF;
    
    SET idInventario = ultimoInventario;
END //
DELIMITER ;

-- SP para insertar inventario (Cuando se realiza conteo manual)
-- Las existencias se actualizan automáticamente cuando se realiza una compra o una venta.

DELIMITER //
CREATE PROCEDURE SP_UPDATE_INVENTORY(
IN codigoProducto INT, 
IN stock INT)
BEGIN
	DECLARE ultimoInventario INT DEFAULT 0;
    DECLARE fechaActual DATE DEFAULT CURDATE();
    DECLARE errorManual INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		IF errorManual = 0 THEN
			ROLLBACK;
			SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Error: No se pudo actualizar el inventario. Verifique e intente de nuevo.';
		END IF;
    END;

	START TRANSACTION;

    CALL SP_ULTIMO_ID_INVENTARIO_FECHA(codigoProducto, @idInventario);
    SET ultimoInventario = (SELECT @idInventario);
    
    IF ultimoInventario <> 0 THEN
		UPDATE INVENTORY 
        SET Inv_Stock = stock , Inv_Date = fechaActual WHERE Inv_ID = ultimoInventario AND Pro_Code = codigoProducto;
	ELSE
		SET errorManual = 1; -- Para que el EXIT HANDLER no la sobreescriba
		ROLLBACK;
		SIGNAL SQLSTATE '02000'
        SET MESSAGE_TEXT = 'Error: No se encontró inventario del producto.';
	END IF;
    
    COMMIT;
END //
DELIMITER ;

-- SP para eliminar inventario (Cuando se realiza conteo manual)
-- Las existencias se actualizan automáticamente cuando se realiza una compra o una venta.

DELIMITER //
CREATE PROCEDURE SP_DELETE_INVENTORY(
IN codigoProducto INT)
BEGIN
	DECLARE ultimoInventario INT DEFAULT 0;
    DECLARE fechaActual DATE DEFAULT CURDATE();    
    DECLARE errorManual INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		IF errorManual = 0 THEN
			ROLLBACK;
			SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Error: No se pudo actualizar el inventario. Verifique e intente de nuevo.';
		END IF;
    END;

	START TRANSACTION;

    CALL SP_ULTIMO_ID_INVENTARIO_FECHA(codigoProducto, @idInventario);
    SET ultimoInventario = (SELECT @idInventario);
    
    IF ultimoInventario <> 0 THEN
		DELETE FROM INVENTORY 
		WHERE Inv_ID = ultimoInventario AND Pro_Code = codigoProducto;
	ELSE
		SET errorManual = 1; -- Para que el EXIT HANDLER no la sobreescriba
		ROLLBACK;
		SIGNAL SQLSTATE '02000'
        SET MESSAGE_TEXT = 'Error: No se encontró inventario del producto.';
	END IF;
    
    COMMIT;
END //
DELIMITER ;

-- SP para la tabla Reserva
DELIMITER //
CREATE PROCEDURE SP_insertarReserva(
    in fecha Date,
    in hora Time,
    in idCliente char(10),
    in promotorId char(10),
    in promocionId int,
    in eventoId int,
    in statusId int
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al insertar la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    INSERT INTO BOOKING(Boo_Date, Boo_Hour, Cus_ID, Mem_ID, Prom_ID, Eve_ID, Sta_ID) VALUES (fecha, hora, idCliente, promotorId, promocionId, eventoId, statusId);

    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_insertarReservaZona(
    in reservaId int,
    in zonaId int
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al insertar la zona de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    INSERT INTO BOOKING_ZONE(Boo_ID, Zon_ID) VALUES (reservaId, zonaId);
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_actualizarFecha(in fecha DATE, in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar la fecha de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    UPDATE BOOKING SET Boo_Date = fecha WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_actualizarHora(in hora TIME, in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar la hora de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    UPDATE BOOKING SET Boo_Hour = hora WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_actualizarZona(in zonaId int, in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar la zona de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    UPDATE BOOKING_ZONE SET Zon_ID = zonaId WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_actualizarStatus(in statusId int, in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar el status de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    UPDATE BOOKING SET Sta_ID = statusId WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_actualizarPromocion(in promocionId int, in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al actualizar la promoción de la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    UPDATE BOOKING SET Prom_ID = promocionId WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_eliminarReserva(in reservaId int)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al eliminar la reserva. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    DELETE FROM BOOKING WHERE Boo_ID = reservaId;
    COMMIT;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_registrarAcompañantes(in reservaId int, in acompañanteId char(10))
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error al registrar el acompañante. Se ha revertido la transacción';
    END;

    START TRANSACTION;
    INSERT INTO BOOKING_CUSTOMER(Boo_ID, Cus_ID) VALUES (reservaId, acompañanteId);
    COMMIT;
END //
DELIMITER ;

-- SP VENTAS
DELIMITER //
CREATE PROCEDURE SP_VENTAS_INSERTAR(
IN IDVENTA INT, 
IN VENTAFECHA DATE,
IN idmiembro CHAR(10), 
IN idcliente CHAR(10),
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La venta no pudo ser insertada.';
	END;
    START TRANSACTION;
		INSERT INTO SALE(Sal_id, Sal_Date, Mem_id, CUS_ID)
		VALUES (IDVENTA, VENTAFECHA, idmiembro, idCliente);
    COMMIT;
END; //
DELIMITER ;


-- SP para actualización de ventas:

DELIMITER //
CREATE PROCEDURE SP_VENTAS_ACTUALIZARCANTIDAD(
IN venta_id INT, 
IN producto_id INT, 
IN newcantidad INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La cantidad de producto vendida no pudo ser actualizada.';
    END;
    START TRANSACTION;
		UPDATE PRODUCT_SALE
		SET ProSale_Quantity = newcantidad
		WHERE Sal_id = venta_id AND Pro_Code = producto_id;
    COMMIT;
END; //
DELIMITER ;

-- SP para eliminación de VENTAS.

DELIMITER //
CREATE PROCEDURE SP_VENTAS_ELIMINAR(
IN venta_id  INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La Venta no pudo ser eliminada.';
    END;
    START TRANSACTION;
		DELETE FROM SALE 
        WHERE Sal_ID=venta_id;

    COMMIT;
END; //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SP_VENTASD_ELIMINAR(
    IN producto_id INT,
IN venta_id  INT,
IN cantidadd int
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: La Venta no pudo ser eliminada.';
    END;
    START TRANSACTION;
        CALL SP_INVENTORY_RECUPERARID(producto_id, @Invid);
        UPDATE Inventory
        SET Inv_Stock = Inv_Stock + cantidadd
        WHERE Inv_ID = @Invid AND Pro_Code = producto_id;
        DELETE FROM PRODUCT_SALE WHERE Sal_ID=venta_id and Pro_Code = producto_id;

    COMMIT;
END; //
DELIMITER ;




DELIMITER //
CREATE PROCEDURE SP_VENTASD_INSERTAR(
IN venta_id  INT,
IN Pro_Codes INT, 
IN cantidad INT
)
BEGIN
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
		ROLLBACK;
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El producto no puede añadirse a la venta.';
    END;
    START TRANSACTION;
		INSERT INTO PRODUCT_SALE(Sal_id, Pro_Code, ProSale_Quantity)
        VALUES (venta_id, Pro_Codes, cantidad);
    COMMIT;
END; //
DELIMITER ;
