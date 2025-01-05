def insert_producto(db):
    nombre = input("Nombre del producto: ")
    precio = input("Precio: ")
    cat_id = input("Id de la categoría (1-10): ")
    conection = db.cursor()
    tupla = (nombre, precio, cat_id)
    sql = "INSERT INTO PRODUCT (Pro_Name, Pro_Price, Cat_ID) VALUES (%s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    print("Producto agregado con éxito.")


def consultar_productos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT")
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        cantidad = fila[3]

        print(f"id: {id_producto} - producto: {nombre} - precio: {precio} - cantidad: {cantidad}")


def actualizar_producto(db):
    conection = db.cursor()
    producto = input("Ingrese el ID del producto a actualizar: ")
    precio = input("Ingrese el precio actualizado: ")

    query = "UPDATE PRODUCT SET Pro_Price=%s WHERE Pro_id=%s"
    values = (precio, producto)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con esa ID.")
    else:
        print(f"Producto actualizado.")


def eliminar_producto(db):
    conection = db.cursor()
    producto = input("Ingrese el ID del producto a eliminar: ")

    query = "DELETE FROM PRODUCT WHERE Pro_Code=%s"
    values = (producto, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con ese ID")
    else:
        print(f"Producto eliminado.")




def menu_crud_productos(db):
    while True:
        print("""
        === Gestión de Productos - Santa Birra===
        1. Insertar Producto
        2. Consultar Productos
        3. Actualizar Producto
        4. Eliminar Producto
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insert_producto(db)

        elif opcion == "2":
            consultar_productos(db)

        elif opcion == "3":

            actualizar_producto(db)


        elif opcion == "4":
            eliminar_producto(db)

        elif opcion == "5":
            break
        else:
            print("Opción no válida.")
