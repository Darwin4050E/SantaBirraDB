def insertar_venta(db):
    conection = db.cursor()
    fecha = input("Por favor ingresa la fecha de la venta (YYYY-MM-DD): ")
    miembro = input("Ingresa el ID del vendedor: ")
    cliente = input("Ingresa la cedula del comprador")
    tupla = (fecha, miembro, cliente)


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


def modificar_venta():
    print("hola")


def eliminar_venta(db):
    conection = db.cursor()
    venta_id = input("Ingrese el ID de la venta que desea eliminar ")

    query = "DELETE FROM SALE WHERE Sal_ID=%s"
    values = (venta_id, )     
    conection.execute(query, values)
    
    query2 = "DELETE FROM PRODUCT_SALE WHERE Sal_ID=%s"
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con ese nombre.")
    else:
        print(f"Producto eliminado.")





def menu_crud_ventas(db):
    while True:
        print("""
        === Gestión de Ventas - Santa Birra ===
        1. Insertar Venta
        2. Consultar Ventas
        3. Modificar Venta
        4. Eliminar Venta
        5. Volver
        """)
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
            print("Opción no válida.")