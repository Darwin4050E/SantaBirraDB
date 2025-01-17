import mensajes as msj
from inputHelper import *
from outputHelper import *
from validadorFK import *
from prettytable import PrettyTable
import mysql.connector as mysql

def insertar_proveedor(db):
    ruc = pedirRUC("RUC del proveedor: ")
    nombre = pedirNombreEmpresa("Nombre del proveedor: ")
    celular = pedirTelefonoConvencional("Teléfono del proveedor: ")
    correo = pedirCorreo("Correo del proveedor: ")

    conection = db.cursor()
    tupla = (ruc, nombre, celular, correo)
    sql = "INSERT INTO SUPPLIER (Sup_RUC, Sup_Name, Sup_Phone, Sup_Email) VALUES (%s, %s, %s, %s)" 
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def consultar_proveedores(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM SUPPLIER")
    tabla = PrettyTable()
    tabla.field_names = ["RUC", "Nombre", "Teléfono", "Correo"]
    datos = conection.fetchall()
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        celular = fila[2]
        correo = fila[3]
        tabla.add_row([cedula, nombre, celular, correo])
    print(tabla)

def actualizar_proveedor(db):
    conection = db.cursor()
    ruc = pedirRUC("RUC del proveedor: ")
    if not validar_clave_foranea(db, "SUPPLIER", "Sup_RUC", ruc):
        printMensajeErrorFK()
        return
    
    nombre = pedirNombreEmpresa("Nombre del proveedor actualizado: ")
    celular = pedirTelefonoConvencional("Celular actualizado: ")
    correo = pedirCorreo("Correo actualizado: ")

    query = "UPDATE SUPPLIER SET Sup_Name=%s,Sup_Phone=%s, Sup_email=%s WHERE Sup_RUC=%s"
    values = (nombre,celular, correo, ruc)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_proveedor(db):
    ruc = pedirRUC("RUC del proveedor: ")

    query = "DELETE FROM SUPPLIER WHERE Sup_RUC=%s"
    values = (ruc,)

    try:
        conection = db.cursor()
        conection.execute(query, values)
        db.commit()
        if conection.rowcount == 0:
            printMensajeErrorFK()
        else:
            printEliminacionExitosa()
    except mysql.Error as e:
        db.rollback()
        print("No se pudo eliminar el proveedor porque hay compras asociadas a él.")

def menu_crud_proveedores(db):
    while True:
        print(msj.opcionesProveedor)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            insertar_proveedor(db)
        elif opcion == "2":
            consultar_proveedores(db) 
        elif opcion == "3":
            consultar_proveedores(db)
            actualizar_proveedor(db)    
        elif opcion == "4":
            consultar_proveedores(db)
            eliminar_proveedor(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
