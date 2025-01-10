from datetime import datetime
from fechaHelper import *
from validadorFK import *
from inputHelper import *
from outputHelper import *
import mensajes as msj

def insert_inventario(db):

    codigoProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codigoProd)):
        printMensajeErrorFK()
        return
    
    idInventario = ultimo_IDProducto(db, codigoProd) + 1
    fecha = getFecha()
    stock = pedirEnteroPositivo("Ingrese el stock del producto: ")
    
    conection = db.cursor()

    sql = "INSERT INTO INVENTORY (Inv_ID, Pro_Code, Inv_Date, Inv_Stock) VALUES (%s, %s, %s, %s) "
    tupla = (idInventario, codigoProd, fecha, stock)
    conection.execute(sql,tupla)

    db.commit()
    printIngresoExitoso()

#Saca el último ID artificial de la secuencia de inventarios del producto
def ultimo_IDProducto(db, idProducto):
    conection = db.cursor()
    if existeInventarioProducto(db, idProducto):
        query = "SELECT Inv_ID FROM INVENTORY WHERE Pro_Code = %s ORDER BY Inv_ID DESC LIMIT 1"
        conection.execute(query, (idProducto, ))
        ic_id = conection.fetchone()
        return int(ic_id[0])
    else:
        return 0

def existeInventarioProducto(db, idProducto):
    conection = db.cursor()
    query = "SELECT COUNT(*) FROM INVENTORY WHERE Pro_Code = %s"
    conection.execute(query, (idProducto, ))
    return conection.fetchone()[0] > 0
    
def consultar_inventario(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INVENTORY ORDER BY Pro_Code, Inv_ID")
    datos = conection.fetchall()
    for fila in datos:
        id_inventario = fila[0]
        codigoProd = fila[1]
        fecha = fila[2].strftime("%d/%m/%Y")
        stock = fila[3]
        print(f"id: {id_inventario} - producto: {codigoProd} - fecha: {fecha} - stock: {stock} ")

def consultar_inventario1(db, id, procode):
    conection = db.cursor()
    conection.execute("SELECT * FROM INVENTORY WHERE Inv_id = %s and Pro_Code= %s", (id,procode ))
    datos = conection.fetchall()
    for fila in datos:
        stock = int(fila[3]) 
        return stock

def obtener_ultimo_inventario(db, codProd):
    conection = db.cursor()
    query = "SELECT Inv_ID FROM INVENTORY WHERE Pro_Code=%s ORDER BY Inv_Date DESC LIMIT 1"
    tupla = (codProd, )
    conection.execute(query, tupla)
    inventario = conection.fetchone()
    if inventario is not None:
        return inventario[0]  # Retorna el ID del inventario
    else:
        return None  # Si no se encontró, retorna None

def actualizar_inventario(db):
    conection = db.cursor()
    codigoProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codigoProd)):
        printMensajeErrorFK()
        return
    
    inventario = obtener_ultimo_inventario(db, codigoProd)
    if inventario is None:
        print("No se encontró inventario del producto.")
        return
    
    stock = pedirEnteroPositivo("Ingrese el nuevo stock del producto: ")

    fechaActual = datetime.today().date() 

    query = "UPDATE INVENTORY SET Inv_Stock=%s, Inv_Date=%s WHERE Inv_ID = %s AND Pro_Code = %s"
    values = (stock, fechaActual, inventario, codigoProd)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

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
    conection = db.cursor()
    #Se eliminará el último inventario
    codProd = pedirIdEntero("Código del producto: ")
    if (not validar_clave_foranea(db, "PRODUCT", "Pro_Code", codProd)):
        printMensajeErrorFK()
        return
    
    inventario = obtener_ultimo_inventario(db, codProd)
    if inventario is None:
        print("No se encontró inventario del producto.")
        return

    query = "DELETE FROM INVENTORY WHERE Inv_ID=%s AND Pro_Code=%s"
    values = (inventario, codProd)
            
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def menu_crud_inventario(db):
    while True:
        print(msj.opcionesInventario)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_inventario(db)
        elif opcion == "2":
            consultar_inventario(db)
        elif opcion == "3":
            consultar_inventario(db)
            actualizar_inventario(db)
        elif opcion == "4":
            consultar_inventario(db)
            eliminar_inventario(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
