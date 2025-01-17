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
