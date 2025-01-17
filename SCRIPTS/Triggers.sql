-- SANTABIRRADB
-- TRIGGERS 
USE SANTABIRRADB;

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

-- Triggers Inventario 
-- Cada vez que se agrega un producto, se le agrega un inventario
DELIMITER //
CREATE TRIGGER TRG_AFTER_INSERT_PRODUCTO
AFTER INSERT ON PRODUCT
FOR EACH ROW
BEGIN 
	INSERT INTO INVENTORY (Inv_ID, Pro_Code, Inv_Date, Inv_Stock) 
    VALUES (1, new.Pro_Code, curdate(), 0);
END //
DELIMITER ;
