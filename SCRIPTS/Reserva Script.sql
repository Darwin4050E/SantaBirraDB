USE SANTABIRRADB;

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