import mensajes as msj
import validadorFK as vfk
import proveedores as prv
import productos as prd
from inputHelper import *
from fechaHelper import *
from prettytable import PrettyTable
import mysql.connector as mysql

def mostrarCodigoCompra(db):
    query = '''
        SELECT DISTINCT Bill_ID 
        FROM Product_Supplier 
        ORDER BY Bill_ID
    '''
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print("")
        for dato in datos:
            print(f"Codigo de compra: {dato[0]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def mostrarRucProveedor(db):
    query = '''
        SELECT DISTINCT Sup_RUC, Sup_Name 
        FROM Supplier 
        ORDER BY Sup_RUC
    '''
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print("")
        for dato in datos:
            print(f"RUC: {dato[0]} - Proveedor: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    
def mostrarRucProveedorAvanzado(db, codigoCompra):
    query = '''
        SELECT DISTINCT Sup_RUC, Sup_Name
        FROM Supplier
        NATURAL JOIN Product_Supplier
        WHERE Bill_ID = %s
        ORDER BY Sup_RUC
    '''
    try:
        cursor = db.cursor()
        cursor.execute(query, (codigoCompra,))
        datos = cursor.fetchall()
        print("")
        for dato in datos:
            print(f"RUC: {dato[0]} - Proveedor: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def mostrarCodigoProducto(db):
    query = '''
        SELECT DISTINCT Pro_Code, Pro_Name 
        FROM Product 
        ORDER BY Pro_Code
    '''
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print("")
        for dato in datos:
            print(f"Código de producto: {dato[0]} - Producto: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def mostrarCodigoProductoAvanzado(db, codigoCompra, rucProveedor):
    query = '''
        SELECT DISTINCT Product.Pro_Code, Pro_Name
        FROM Product
        NATURAL JOIN Product_Supplier
        WHERE Bill_ID = %s AND Sup_RUC = %s
        ORDER BY Pro_Code
    '''
    try:
        cursor = db.cursor()
        cursor.execute(query, (codigoCompra, rucProveedor))
        datos = cursor.fetchall()
        print("")
        for dato in datos:
            print(f"Código de producto: {dato[0]} - Producto: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def solicitarDatosCompra(db):
    
    mostrarCodigoCompra(db)
    codigoCompra = pedirIdEntero("\nIngrese el código de la compra: ")
    
    mostrarRucProveedor(db)
    rucProveedor = pedirRUC("\nIngrese el RUC del proveedor: ")
    while(not vfk.validar_clave_foranea(db, "Supplier", "Sup_RUC", rucProveedor)):
        mostrarRucProveedor(db)
        rucProveedor = pedirRUC("\nIngrese el RUC del proveedor: ")
    
    mostrarCodigoProducto(db)
    codigoProducto = pedirIdEntero("\nIngrese el código del producto: ")
    while(not vfk.validar_clave_foranea(db, "Product", "Pro_Code", codigoProducto)):
        mostrarCodigoProducto(db)
        codigoProducto = pedirIdEntero("\nIngrese el código del producto: ")
        
    return [codigoCompra, rucProveedor, codigoProducto]

def solicitarDatosCompraAvanzados(db):
        
    mostrarCodigoCompra(db)
    codigoCompra = pedirIdEntero("\nIngrese el código de la compra: ")
    
    mostrarRucProveedorAvanzado(db, codigoCompra)
    rucProveedor = pedirRUC("\nIngrese el RUC del proveedor: ")
    while(not vfk.validar_clave_foranea(db, "Supplier", "Sup_RUC", rucProveedor)):
        mostrarRucProveedorAvanzado(db, codigoCompra)
        rucProveedor = pedirRUC("\nIngrese el RUC del proveedor: ")
    
    mostrarCodigoProductoAvanzado(db, codigoCompra, rucProveedor)
    codigoProducto = pedirIdEntero("\nIngrese el código del producto: ")
    while(not vfk.validar_clave_foranea(db, "Product", "Pro_Code", codigoProducto)):
        mostrarCodigoProductoAvanzado(db, codigoCompra, rucProveedor)
        codigoProducto = pedirIdEntero("\nIngrese el código del producto: ")

        
    return [codigoCompra, rucProveedor, codigoProducto]

def insertarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompra(db)  
    fechaCompra = getFecha()
    cantidadComprada = pedirNatural("\nIngrese la cantidad de producto comprada: ")
    
    try:
        cursor = db.cursor()
        cursor.callproc('SP_COMPRAS_INSERTAR', (codigoCompra, rucProveedor, codigoProducto, fechaCompra, cantidadComprada))
        print("\nCompra agregada con éxito.")
    except mysql.Error as e:
        print(e)
    finally:
        cursor.close()

def consultarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompraAvanzados(db)
    
    try:
        cursor = db.cursor()
        tabla = PrettyTable()
        tabla.field_names = ["Codigo Compra", "Ruc Proveedor","Fecha", "Codigo Producto", "Cantidad"]
        cursor.callproc('SP_COMPRAS_CONSULTAR', (codigoCompra, rucProveedor, codigoProducto))
        resultados = cursor.stored_results()
        for resultado in resultados:
            dato = resultado.fetchall()
            fecha = dato[0][0]
            cantidad = dato[0][1]
            tabla.add_row([codigoCompra, rucProveedor,fecha , codigoProducto, cantidad])
        print(tabla)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def actualizarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompraAvanzados(db)
    
    print(msj.opcionesActualizacionCommpra)
    opciones = [1,2]
    opcion = input("Ingrese una opción: ")
    while ((not opcion.isdigit()) or (int(opcion) not in opciones)):
        print("Ingrese una opción válida.")
        opcion = input("Ingrese una opción: ")
    opcion = int(opcion)
        
    valor = ""
    if(opcion == 1):
        valor = getFecha()
    else:
        valor = pedirNatural("\nIngrese la nueva cantidad de producto comprada: ")
    
    try:
        cursor = db.cursor()
        if(opcion == 1):
            cursor.callproc('SP_COMPRAS_ACTUALIZARFECHA', (codigoCompra, rucProveedor, codigoProducto, valor))
        else:
            cursor.callproc('SP_COMPRAS_ACTUALIZARCANTIDAD', (codigoCompra, rucProveedor, codigoProducto, valor))
        print("\nCompra actualizada con éxito.")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def eliminarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompraAvanzados(db)
    
    try:
        cursor = db.cursor()
        cursor.callproc('SP_COMPRAS_ELIMINAR', [codigoCompra, rucProveedor, codigoProducto])
        print("\nCompra eliminada con éxito.")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def menu_crud_compras(db):
    while True:
        print(msj.opcionesCompra)
        opcion = int(input("Seleccione una opción [1-5]: "))
        if(opcion == 1):
            insertarCompra(db)
        elif(opcion == 2):
            consultarCompra(db)
        elif(opcion == 3):
            actualizarCompra(db)
        elif(opcion == 4):
            eliminarCompra(db)
        elif(opcion == 5):
            return
        else:
            print(msj.opcionesError)