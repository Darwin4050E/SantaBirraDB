import mensajes as msj
import validadorFK as vfk
import proveedores as prv
import productos as prd
from inputHelper import *
from fechaHelper import *

def mostrarCodigoCompra(db):
    query = 'SELECT DISTINCT Bill_ID FROM Product_Supplier ORDER BY Bill_ID'
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
    query = 'SELECT DISTINCT Sup_RUC, Sup_Name FROM Supplier ORDER BY Sup_RUC'
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
    query = 'SELECT DISTINCT Pro_Code, Pro_Name FROM Product ORDER BY Pro_Code'
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

    primeraQuery = '''
        INSERT INTO Product_Supplier (Pro_Code, Sup_RUC, Bill_ID, Bill_Date, Bill_Quantity)
        VALUES (%s, %s, %s, %s, %s)
    '''
    segundaQuery = '''
        UPDATE Inventory
        SET Inv_Stock = Inv_Stock + %s
        WHERE Pro_Code = %s AND Inv_Date = %s
    '''
    
    try:
        cursor = db.cursor()
        cursor.execute(primeraQuery, (codigoProducto, rucProveedor, codigoCompra, fechaCompra, cantidadComprada))
        cursor.execute(segundaQuery, (cantidadComprada, codigoProducto, fechaCompra))
        db.commit()
        print("\nCompra agregada con éxito.")    
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def consultarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompraAvanzados(db)
    
    query = '''
        SELECT Bill_Date, Bill_Quantity
        FROM Product_Supplier
        WHERE Bill_ID = %s AND Sup_RUC = %s AND Pro_Code = %s
    '''
    
    try:
        cursor = db.cursor()
        cursor.execute(query, (codigoCompra, rucProveedor, codigoProducto))
        datos = cursor.fetchall()
        print(f"\nFecha de la compra: {str(datos[0][0])} - Cantidad de producto comprada: {datos[0][1]}")
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
        
    campo = ""
    valor = ""
    if(opcion == 1):
        campo = "Bill_Date"
        valor = getFecha()
    else:
        campo = "Bill_Quantity"
        valor = pedirNatural("Ingrese la nueva cantidad de producto comprada: ")
    
    primeraQuery = '''
        UPDATE Product_Supplier
        SET {} = %s
        WHERE Bill_ID = %s AND Sup_RUC = %s AND Pro_Code = %s
    '''.format(campo)
    segundaQuery = '''
        SELECT Bill_Date, Bill_Quantity
        FROM Product_Supplier
        WHERE Bill_ID = %s AND Sup_RUC = %s AND Pro_Code = %s
    '''
    
    try:
        cursor = db.cursor()
        cursor.execute(primeraQuery, (valor, codigoCompra, rucProveedor, codigoProducto))
        cursor.execute(segundaQuery, (codigoCompra, rucProveedor, codigoProducto))
        datos = cursor.fetchall()
        if(opcion == 1):
            queryActualizarFechaInventario = '''
                UPDATE Inventory
                SET Inv_Date = %s
                WHERE Pro_Code = %s AND Inv_Date = %s
            '''
            cursor.execute(queryActualizarFechaInventario, (valor, codigoProducto, str(datos[0][0])))
            db.commit()
        else:
            queryActualizarStockInventario = '''
                UPDATE Inventory
                SET Inv_Stock = Inv_Stock + %s
                WHERE Pro_Code = %s AND Inv_Date = %s
            '''
            cursor.execute(queryActualizarStockInventario, (valor - int(datos[0][1]), codigoProducto, str(datos[0][0])))
            db.commit()
        print("\nCompra actualizada con éxito.")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def eliminarCompra(db):
    
    codigoCompra, rucProveedor, codigoProducto = solicitarDatosCompraAvanzados(db)
        
    primeraQuery = '''
        SELECT Bill_Date, Bill_Quantity
        FROM Product_Supplier
        WHERE Bill_ID = %s AND Sup_RUC = %s AND Pro_Code = %s
    '''
    terceraQuery = '''
        DELETE FROM Product_Supplier
        WHERE Bill_ID = %s AND Sup_RUC = %s AND Pro_Code = %s
    '''
    
    try:
        cursor = db.cursor()
        cursor.execute(primeraQuery, (codigoCompra, rucProveedor, codigoProducto))
        datos = cursor.fetchall()
        segundaQuery = '''
            UPDATE Inventory
            SET Inv_Stock = Inv_Stock - %s
            WHERE Pro_Code = %s AND Inv_Date = %s
        '''
        cursor.execute(segundaQuery, (int(datos[0][1]), codigoProducto, str(datos[0][0])))
        cursor.execute(terceraQuery, (codigoCompra, rucProveedor, codigoProducto))
        db.commit()
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