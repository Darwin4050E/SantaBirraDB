import mensajes as msj
import clientes
import productos
import miembros
import productos
import inventario

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
        productoss.append(producto)
        cantidades.append(cantidad)
        pro_eleccion = input("Ingrese N si desea terminar de añadir productos: ")

    tupla = (numero, fecha, miembro, cliente)
    sql = "INSERT INTO SALE (Sal_id, Sal_Date, Mem_id, CUS_ID) VALUES (%s, %s, %s, %s)" 
    conection.execute(sql,tupla)
    db.commit()
    for i in range(len(productoss)):
        tupla1 = (numero, productoss[i], cantidades[i])
        query2 = "INSERT INTO PRODUCT_SALE (Sal_id, Pro_code, ProSale_Quantity) VALUES (%s, %s, %s)"
        conection.execute(query2,tupla1)
        db.commit()
        inventario_id = inventario.obtener_ultimo_inventario(db, productoss[i])
        nuevo_stock = inventario.consultar_inventario1(db, inventario_id) - int(cantidades[i])
        inventario.actualizarstock_inventario(db, inventario_id, nuevo_stock)

def consultar_ventas(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM SALE")
    datos = conection.fetchall()
    for fila in datos:
        id_venta = fila[0]
        fecha = fila[1].strftime('%d/%m/%Y') 
        vendedor_id = fila[2]
        cliente_id = fila[3]
        print(f"(Num. venta: {id_venta}, fecha: {fecha}, ID Vendedor :'{vendedor_id}', ' ID Cliente: {cliente_id}')")
    
    eleccion = input("Ingrese S si desea consultar los detalles de una venta: ")
    if eleccion == "S":
        venta = int(input("Ingrese el ID de la venta: "))
        tupla = (venta,)
        query = "SELECT * FROM PRODUCT_SALE WHERE Sal_id = %s"
        conection.execute(query, tupla)
        datos = conection.fetchall()
        for i in datos:
            id_p = i[1]
            cantidad = i[2]
            print(productos.consultar_producto(db, id_p) + " - cantidad:" + str(cantidad))  

def modificar_venta():
    print("hola")

def eliminar_venta(db):
    conection = db.cursor()
    venta_id = input("Ingrese el ID de la venta que desea eliminar ")
    values = (venta_id, )     
    query2 = "DELETE FROM PRODUCT_SALE WHERE Sal_ID=%s"
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