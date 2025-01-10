import mensajes as msj
import inventario

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

def consultar_productos_ex(db, ids):
    conection = db.cursor()
    ids =(ids)
    if len(ids) == 1:
         query = "SELECT * FROM PRODUCT WHERE Pro_code != %s"
         conection.execute(query, (ids[0],))  # Pasamos el solo valor como tupla
    else:
        query = "SELECT * FROM PRODUCT WHERE Pro_code NOT IN (%s)" % ','.join(['%s'] * len(ids))
        conection.execute(query, tuple(ids))
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        inv = inventario.obtener_ultimo_inventario(db, id_producto)
        cantidad = inventario.consultar_inventario1(db, inv, id_producto)
        print(f"id: {id_producto} - producto: {nombre} - precio: {precio} - cantidad: {cantidad}")

def consultar_productos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT")
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        inv = inventario.obtener_ultimo_inventario(db, id_producto)
        cantidad = inventario.consultar_inventario1(db, inv, id_producto)
        print(f"id: {id_producto} - producto: {nombre} - precio: {precio} - cantidad: {cantidad}")

def consultar_producto(db, id):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT WHERE Pro_code = %s", (id, ))
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        return f"producto: {nombre} - precio: {precio}" 

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
        print(msj.opcionesProducto)
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
            print(msj.opcionesError)