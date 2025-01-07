import mensajes as msj
import validadorFK as vfk

def solicitarDatosCompra(db):
    
    codigoCompra = int(input("Ingrese el código de la compra: "))
    while(codigoCompra < 1000 or codigoCompra > 9999):
        codigoProducto = int(input("Ingrese un código de compra correcto: "))
    
    rucProveedor = input("Ingrese el RUC del proveedor: ")
    while(not vfk.validar_clave_foranea(db, "Supplier", "Sup_RUC", rucProveedor)):
        rucProveedor = int(input("Ingrese un RUC de proveedor correcto: "))
    
    codigoProducto = int(input("Ingrese el código del producto: "))
    while(not vfk.validar_clave_foranea(db, "Product", "Pro_Code", codigoProducto)):
        codigoProducto = int(input("Ingrese un código de producto correcto: "))

def insertarCompra(db):
    
    codigoCompra, codigoProducto, rucProveedor = solicitarDatosCompra(db)
      
    fechaCompra = input("Ingrese la fecha de la compra [YYYY-MM-DD]: ")
    while(len(fechaCompra) != 10):
        fechaCompra = input("Ingrese la fecha en el formato correcto [YYYY-MM-DD]: ")
           
    cantidadComprada = int(input("Ingrese la cantidad de producto comprada: "))
    while(cantidadComprada <= 0):
        cantidadComprada = input("Ingrese una cantidad correcta: ")
        
    query = f'INSERT INTO Product_Supplier VALUES ({codigoProducto}, {rucProveedor}, {codigoCompra}, {fechaCompra}, {cantidadComprada})'

    try:
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        print("Compra agregada con éxito.")    
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def consultarCompra(db):
    
    codigoCompra, codigoProducto, rucProveedor = solicitarDatosCompra(db)
    
    query = f'SELECT Bill_Date, Bill_Quantity FROM Product_Supplier WHERE Bill_ID = {codigoCompra} AND Sup_RUC = {rucProveedor} AND Pro_Code = {codigoProducto}'

    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print(f"Fecha de la compra: {datos[0]} - Cantidad de producto comprada: {datos[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def eliminarCompra(db):
    
    codigoCompra, codigoProducto, rucProveedor = solicitarDatosCompra(db)
        
    primeraQuery = f'SELECT Bill_Quantity, Bill_Date FROM Product_Supplier WHERE Bill_ID = {codigoCompra} AND Sup_RUC = {rucProveedor} AND Pro_Code = {codigoProducto}'
    terceraQuery = f'DELETE FROM Product_Supplier WHERE Bill_ID = {codigoCompra} AND Sup_RUC = {rucProveedor} AND Pro_Code = {codigoProducto}'
    
    try:
        cursor = db.cursor()
        cursor.execute(primeraQuery)
        datos = cursor.fetchall()
        segundaQuery = f'UPDATE Inventory SET Inv_Stok = Inv_Stock - {datos[0]} WHERE Pro_Code = {codigoProducto} AND Bill_Date = {datos[1]}'
        cursor.execute(segundaQuery)
        cursor.execute(terceraQuery)
        print("Compra eliminada con éxito.")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def menu_crud_ventas(db):
    while True:
        print(msj.opcionesCompra)
        opcion = int(input("Seleccione una opción [1-4]: "))
        if(opcion == 1):
            insertarCompra(db)
        elif(opcion == 2):
            consultarCompra(db)
        elif(opcion == 3):
            eliminarCompra(db)
        elif(opcion == 4):
            return
        else:
            print(msj.opcionesError)