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
from prettytable import PrettyTable

def insertar_venta(db):
    conection = db.cursor()
    print("\nVentas realizadas: ")
    consultar_ventas_sin(db)
    numero = pedirIdEntero("Número de la venta actual: ")
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

    
    errores = 0
    
    conection.callproc('SP_VENTAS_INSERTAR', (numero,fecha, miembro, cliente))
    for i in range(len(productoss)):
        productoo, cantidadess = productoss[i], cantidades[i]
        try:
           conection.callproc('SP_VENTASD_INSERTAR', (numero, productoo, cantidadess))
        except Exception as e:
            print(e)
            errores += 1 
    if errores == len(productoss):
        conection.callproc('SP_VENTAS_ELIMINAR', (numero,))
    db.commit()
    
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
    tabla = PrettyTable()
    tabla.field_names = ["ID Venta", "Fecha", "ID Vendedor", "ID Cliente"]
    datos = conection.fetchall()
    for fila in datos:
        id_venta = fila[0]
        fecha = fila[1].strftime('%d/%m/%Y') 
        vendedor_id = fila[2]
        cliente_id = fila[3]
        tabla.add_row([id_venta, fecha, vendedor_id, cliente_id])
    print(tabla)

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
    conection = db.cursor()
    venta = pedirIdEntero("Ingrese el ID de la venta que desea modificar: ")
    if not validar_clave_foranea(db, "SALE", "Sal_ID", venta):
        printMensajeErrorFK()
        return
    dato1, dato2 = consultar_venta(db, venta)
    for i in range(len(dato1)):
        id_p = dato1[i]
        cantidad = dato2[i]
        print(str(id_p) + " " + productos.consultar_producto(db, id_p) + " - cantidad:" + str(cantidad))
    eleccion = pedirIdEntero("Ingresa el ID del producto al que deseas cambiar la cantidad: ")
    eleccion2 = pedirIdEntero("Ingresa la cantidad a modificar: ")
    try:
        conection.callproc('SP_VENTAS_ACTUALIZARCANTIDAD', (venta,eleccion, eleccion2))
    except Exception as e:
        print(e)


def eliminar_venta(db):
    conection = db.cursor()
    consultar_ventas_sin(db)
    venta_id = pedirIdEntero("Ingrese el ID de la venta que desea eliminar: ")
    if not validar_clave_foranea(db, "SALE", "Sal_ID", venta_id):
        printMensajeErrorFK()
        return
    try:
        print(venta_id)
        productoss, cantidadess = consultar_venta(db, venta_id)
        for i in range(len(productoss)):
            conection.callproc('SP_VENTASD_ELIMINAR', (productoss[i], venta_id, cantidadess[i]))
        conection.callproc('SP_VENTAS_ELIMINAR', (venta_id,))
        db.commit()
        print("\nVenta eliminada con éxito.")
    except Exception as e:
        print(e)
    finally:
        conection.close()


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