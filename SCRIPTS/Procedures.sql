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


