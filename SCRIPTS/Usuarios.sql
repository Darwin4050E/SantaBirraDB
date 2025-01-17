-- SANTABIRRADB
-- USERS - PERMISOS
USE SANTABIRRADB;

-- Usuarios:

CREATE USER 'manager_user'@'%' IDENTIFIED BY 'ManPas001';

-- Permisos a usuarios:

GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_INSERTAR TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_CONSULTAR TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ACTUALIARFECHA TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ACTUALIZARCANTIDAD TO 'manager_user'@'%';
GRANT EXECUTE ON PROCEDURE SANTABIRRADB.SP_COMPRAS_ELIMINAR TO 'manager_user'@'%';

GRANT EXECUTE ON SANTABIRRADB.VW_COMPRAS_GASTOSPROVEEDOR TO 'manager_user'@'%';