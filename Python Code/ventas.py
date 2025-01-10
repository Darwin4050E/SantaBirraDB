import mensajes as msj
import clientes
import productos
import productos
import inventario

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
    numero = input("Por favor ingresa el número de venta:")
    fecha = input("Por favor ingresa la fecha de la venta (YYYY-MM-DD): ")

    vendedores = "SELECT * FROM SELLER JOIN MEMBER USING(MEM_ID)"
    conection.execute(vendedores)
    datos = conection.fetchall()
    for i in datos:
      print(i)
    miembro = input("Ingresa el ID del vendedor: ")
    clientes.consultar_clientes(db)
    cliente = input("Ingresa la cedula del comprador: ")
    pro_eleccion = ""
    productoss = []
    cantidades = []
    while pro_eleccion !="N":
        productos.consultar_productos(db)
        producto = input("Ingrese el ID del producto: ")
        
        cantidad = input("Ingrese la cantidad: ")
        if producto in productoss:
            print("Ingrese un producto que no esté en la compra:")
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
        print(f"(Num. venta: {id_venta}, fecha: {fecha}, ID Vendedor :'{vendedor_id}', ' ID Cliente: {cliente_id}')")

def consultar_ventas(db):
    consultar_ventas_sin(db)
    eleccion = input("Ingrese S si desea consultar los detalles de una venta: ")
    if eleccion == "S":
        venta = int(input("Ingrese el ID de la venta: "))
        dato1, dato2 = consultar_venta(db, venta)
        for i in range(len(dato1)):
            id_p = dato1[i]
            cantidad = dato2[i]
            print(productos.consultar_producto(db, id_p) + " - cantidad:" + str(cantidad))  

def modificar_venta(db):
    consultar_ventas_sin(db)
    venta = int(input("Ingrese el ID de la venta que va a modificar: "))
    pro_eleccion = ""
    productoss = []
    cantidades = []
    productos.consultar_productos_ex(db, ids)
    while pro_eleccion !="N":
        ids, data = consultar_venta(db, venta)
        producto = input("Ingrese el ID del producto a añadir a la venta: ")
        cantidad = input("Ingrese la cantidad: ")
        productoss.append(producto)
        cantidades.append(cantidad)
        pro_eleccion = input("Ingrese N si desea terminar de añadir productos: ")
    for i in range(len(productoss)):
        productoo, cantidadess = productoss[i], cantidades[i]
        restar(db, venta, productoo, cantidadess)


def eliminar_venta(db):
    conection = db.cursor()
    venta_id = input("Ingrese el ID de la venta que desea eliminar ")
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