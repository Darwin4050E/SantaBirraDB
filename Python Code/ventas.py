import mensajes as msj
import clientes
import productos
import productos
import inventario
from inputHelper import *
from outputHelper import *
from validadorFK import *
from fechaHelper import *
from miembros import *


def restar(db, numero, productoo, cantidadess):
        conection = db.cursor()
        tupla1 = (numero, productoo, cantidadess)
        query2 = "INSERT INTO PRODUCT_SALE (Sal_id, Pro_code, ProSale_Quantity) VALUES (%s, %s, %s)"
        conection.execute(query2,tupla1)
        db.commit()
        inventario_id = inventario.obtener_ultimo_inventario(db, productoo)
        nuevo_stock = inventario.consultar_inventario1(db, inventario_id, productoo) - int(cantidadess)
        inventario.actualizarstock_inventario(db, inventario_id, productoo, nuevo_stock)

def sumar(db, productoo, cantidadess):
        inventario_id = inventario.obtener_ultimo_inventario(db, productoo)
        nuevo_stock = inventario.consultar_inventario1(db, inventario_id, productoo) + int(cantidadess)
        inventario.actualizarstock_inventario(db, inventario_id, productoo, nuevo_stock)

def insertar_venta(db):
    conection = db.cursor()
    numero = pedirIdEntero("Número de la venta: ")
    if validar_clave_foranea(db, "SALE", "Sal_ID", numero):
        printMensajeIngresoExistente()
        return
    
    fecha = getFecha()

    miembro = pedirVendedor(db)
    cliente = pedirCliente(db)
    pro_eleccion = ""
    productoss = []
    cantidades = []
    while pro_eleccion !="N":
        producto = pedirProducto(db)
        
        cantidad = pedirNatural("Cantidad: ")
        if producto in productoss:
            print("Ingrese un producto que no esté en la compra.")
        else:
            productoss.append(producto)
            cantidades.append(cantidad)

        pro_eleccion = input("Ingrese N si desea terminar de añadir productos: ")

    tupla = (numero, fecha, miembro, cliente)
    sql = "INSERT INTO SALE (Sal_id, Sal_Date, Mem_id, CUS_ID) VALUES (%s, %s, %s, %s)" 
    conection.execute(sql,tupla)
    db.commit()
    for i in range(len(productoss)):
        productoo, cantidadess = productoss[i], cantidades[i]
        restar(db, numero, productoo, cantidadess)

def pedirVendedor(db):
    print("\nVendedores disponibles: ")
    consultar_empleadosPorRol(db, "SELLER")
    vendedor = pedirCedula("Cédula del vendedor: ")
    while not validar_clave_foranea(db, "SELLER", "Mem_ID", vendedor):
        print("Ingrese un vendedor válido.")
        vendedor = pedirCedula("Cédula del vendedor: ")
    return vendedor

def pedirCliente(db):
    print("\nClientes disponibles: ")
    clientes.consultar_clientes(db)
    cliente = pedirCedula("Cédula del cliente: ")
    while not validar_clave_foranea(db, "CUSTOMER", "CUS_ID", cliente):
        print("Ingrese un cliente válido.")
        cliente = pedirCedula("Cédula del cliente: ")
    return cliente

def pedirProducto(db):
    print("\nProductos disponibles: ")
    productos.consultar_productosSinInventario(db)
    producto = pedirIdEntero("ID del producto: ")
    while not validar_clave_foranea(db, "PRODUCT", "Pro_code", producto):
        print("Ingrese un producto válido.")
        producto = pedirIdEntero("ID del producto: ")
    return producto

def pedirProductoSinMostrar(db):
    producto = pedirIdEntero("ID del producto: ")
    while not validar_clave_foranea(db, "PRODUCT", "Pro_code", producto):
        print("Ingrese un producto válido.")
        producto = pedirIdEntero("ID del producto: ")
    return producto

def consultar_venta(db, id):
    conection = db.cursor()
    tupla = (id,)
    query = "SELECT * FROM PRODUCT_SALE WHERE Sal_id = %s"
    conection.execute(query, tupla)
    datos = conection.fetchall()
    id_ps = []
    cans = []
    for i in datos:
        id_p = i[1]
        cantidad = i[2]
        id_ps.append(id_p)
        cans.append(cantidad)
    return id_ps, cans

def consultar_ventas_sin(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM SALE")
    datos = conection.fetchall()
    for fila in datos:
        id_venta = fila[0]
        fecha = fila[1].strftime('%d/%m/%Y') 
        vendedor_id = fila[2]
        cliente_id = fila[3]
        print(f"Num. venta: {id_venta} - fecha: {fecha} - ID Vendedor :{vendedor_id} - ID Cliente: {cliente_id}")


def consultar_ventas(db):
    consultar_ventas_sin(db)
    venta = pedirIdEntero("Ingrese el ID de la venta que desea consultar: ")
    if not validar_clave_foranea(db, "SALE", "Sal_ID", venta):
        printMensajeErrorFK()
        return
        
    dato1, dato2 = consultar_venta(db, venta)
    for i in range(len(dato1)):
        id_p = dato1[i]
        cantidad = dato2[i]
        print(productos.consultar_producto(db, id_p) + " - cantidad:" + str(cantidad))  

def modificar_venta(db):
    consultar_ventas_sin(db)
    venta = pedirIdEntero("Ingrese el ID de la venta que desea modificar: ")
    if not validar_clave_foranea(db, "SALE", "Sal_ID", venta):
        printMensajeErrorFK()
        return
    
    productoss = []
    cantidades = []
    dato1, dato2 = consultar_venta(db, venta)
    dato1 = tuple(dato1)
    productos.consultar_productos_ex(db, dato1)
    pro_eleccion = ""
    while pro_eleccion !="N":
        ids, data = consultar_venta(db, venta)
        producto = pedirProductoSinMostrar(db)
        cantidad = pedirNatural("Cantidad: ")
        productoss.append(producto)
        cantidades.append(cantidad)
        pro_eleccion = input("Ingrese N si desea terminar de añadir productos: ")
    for i in range(len(productoss)):
        productoo, cantidadess = productoss[i], cantidades[i]
        restar(db, venta, productoo, cantidadess)


def eliminar_venta(db):
    conection = db.cursor()
    consultar_ventas_sin(db)
    venta_id = pedirIdEntero("Ingrese el ID de la venta que desea eliminar: ")
    if not validar_clave_foranea(db, "SALE", "Sal_ID", venta_id):
        printMensajeErrorFK()
        return
    
    values = (venta_id, )     
    query2 = "DELETE FROM PRODUCT_SALE WHERE Sal_ID=%s"
    dato1 , dato2 = consultar_venta(db, venta_id)
    for i in range(len(dato1)):
        sumar(db, dato1[i], dato2[i])


    conection.execute(query2, values)
    db.commit()
    query = "DELETE FROM SALE WHERE Sal_ID=%s"
    values = (venta_id, )     
    conection.execute(query, values)
    query2 = "DELETE FROM PRODUCT_SALE WHERE Sal_ID=%s"
    conection.execute(query2, values)
    db.commit()

def menu_crud_ventas(db):
    while True:
        print(msj.opcionesVenta)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insertar_venta(db)
        elif opcion == "2":
            consultar_ventas(db)
        elif opcion == "3":
            modificar_venta(db)
        elif opcion == "4":
            eliminar_venta(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)