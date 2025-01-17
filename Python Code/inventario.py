from datetime import datetime
from fechaHelper import *
from validadorFK import *
from inputHelper import *
from outputHelper import *
import mensajes as msj
import productos as prod
import mysql.connector as mysql
from prettytable import PrettyTable


def insert_inventario(db):
    prod.consultar_productosSinInventario(db)

    codigoProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codigoProd)):
        printMensajeErrorFK()
        return
    
    fecha = getFecha()
    stock = pedirEnteroPositivo("Stock del producto: ")
    
    conection = db.cursor()

    try:
        conection.callproc('SP_INSERTAR_INVENTORY', (codigoProd, fecha, stock))
        printIngresoExitoso()
    except mysql.Error as e:
        print(e)
    finally:
        conection.close()


def consultar_inventario(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INVENTORY ORDER BY Pro_Code, Inv_ID")
    datos = conection.fetchall()
    # Crear la tabla
    tabla = PrettyTable()
    tabla.field_names = ["ID Inventario", "ID Producto", "Fecha", "Stock"]

    for fila in datos:
        id_inventario = fila[0]
        codigoProd = fila[1]
        fecha = fila[2].strftime("%d/%m/%Y")
        stock = fila[3]
        tabla.add_row([id_inventario, codigoProd, fecha, stock])

    # Mostrar la tabla
    print(tabla)
    conection.close()

def consultar_inventario1(db, id, procode):
    conection = db.cursor()
    conection.execute("SELECT * FROM INVENTORY WHERE Inv_id = %s and Pro_Code= %s", (id,procode ))
    datos = conection.fetchall()
    for fila in datos:
        stock = int(fila[3]) 
        return stock

def actualizar_inventario(db):
    consultar_inventario(db)
    conection = db.cursor()
    codigoProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codigoProd)):
        printMensajeErrorFK()
        return
    
    stock = pedirEnteroPositivo("Ingrese el nuevo stock del producto: ")
    
    try: 
        conection.callproc('SP_UPDATE_INVENTORY', (codigoProd, stock))
        printActualizacionExitosa()
    except mysql.Error as e:
        print(e.msg)
    finally:
        conection.close()


def actualizarstock_inventario(db, id, pro, stock):
    conection = db.cursor()

    query = "UPDATE INVENTORY SET Inv_Stock=%s WHERE Inv_ID = %s and Pro_code = %s"
    values = (stock, id, pro)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con ese ID.")
    else:
        print(f"Inventario actualizado.")

def eliminar_inventario(db):
    consultar_inventario(db)
    conection = db.cursor()
    codigoProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codigoProd)):
        printMensajeErrorFK()
        return
    
    try: 
        conection.callproc('SP_DELETE_INVENTORY', (codigoProd, ))
        printEliminacionExitosa()
    except mysql.Error as e:
        print(e.msg)
    finally:
        conection.close()

def menu_crud_inventario(db):
    while True:
        print(msj.opcionesInventario)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_inventario(db)
        elif opcion == "2":
            consultar_inventario(db)
        elif opcion == "3":
            actualizar_inventario(db)
        elif opcion == "4":
            eliminar_inventario(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
