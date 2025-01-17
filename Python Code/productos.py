import mensajes as msj
import inventario
from inputHelper import *
from outputHelper import *
from fechaHelper import *
from validadorFK import *
import mysql.connector as mysql
from prettytable import PrettyTable



def insert_producto(db):
    mostrarCategorias(db)
    cat_id = pedirIdEntero("ID de la categoría: ")
    if not validar_clave_foranea(db, "CATEGORYPROD", "Cat_ID", cat_id):
        printMensajeErrorFK()
        return
    
    nombre = pedirNombreConSignos("Nombre del producto: ")
    precio = pedirDecimalPositivo("Precio del producto: ")
    unidadMedida = pedirUnidadMedidad("Unidad de medida del producto: ")

    conection = db.cursor()
    try: 
        tupla = (nombre, precio, cat_id, unidadMedida)
        sql = "INSERT INTO PRODUCT (Pro_Name, Pro_Price, Cat_ID, Pro_UnitSize) VALUES (%s, %s, %s, %s) "
        conection.execute(sql,tupla)
        db.commit()
        printIngresoExitoso()
    except mysql.Error as e:
        print(e.msg)

def mostrarCategorias(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM CATEGORYPROD")
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Categoría"]
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        tabla.add_row([id_producto, nombre])
    print(tabla)

def pedirCategoria(db):
    mostrarCategorias(db)
    cat_id = pedirIdEntero("ID de la categoría actual: ")
    while not validar_clave_foranea(db, "CATEGORYPROD", "Cat_ID", cat_id):
        printMensajeErrorFK()
        cat_id = pedirIdEntero("ID de la categoría actual: ")
    return cat_id

def consultar_productos_ex(db, ids):
    conection = db.cursor()
    

    if len(ids) == 1:
        query = "SELECT * FROM PRODUCT WHERE Pro_code != %s"
        conection.execute(query, (ids[0],))  # Pasamos el único valor como tupla
    elif len(ids) > 1:
        placeholders = ','.join(['%s'] * len(ids))  # Crea un marcador para cada ID
        query = f"SELECT * FROM PRODUCT WHERE Pro_code NOT IN ({placeholders})"
        conection.execute(query, tuple(ids))
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        inv = inventario.obtener_ultimo_inventario(db, id_producto)
        cantidad = inventario.consultar_inventario1(db, inv, id_producto)
        print(f"id: {id_producto} - producto: {nombre} - precio: {precio} - cantidad: {cantidad}")

def consultar_productosConInventario(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT")
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Producto", "Precio", "Unidad", "ID Categoría", "Cantidad"]
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        inv = inventario.obtener_ultimo_inventario(db, id_producto)
        cantidad = inventario.consultar_inventario1(db, inv, id_producto)
        idCategoria = fila[3]
        unidad = fila[4]
        tabla.add_row([id_producto, nombre, precio, unidad, idCategoria, cantidad])
    print(tabla)

def consultar_productosSinInventario(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT NATURAL JOIN CATEGORYPROD ORDER BY Pro_code")
    tabla = PrettyTable()  
    tabla.field_names = ["ID", "Producto", "Precio", "Unidad", "ID Categoría", "Categoría"]
    datos = conection.fetchall()
    for fila in datos:
        id_categoria = fila[0]
        id_producto = fila[1]
        nombre = fila[2]
        precio = fila[3] 
        unidad = fila[4]
        categoriaNombre = fila[5]
        tabla.add_row([id_producto, nombre, precio, unidad, id_categoria, categoriaNombre])
    print(tabla)

def consultar_UnSoloProducto(db, id):
    conection = db.cursor()
    conection.execute("SELECT * FROM PRODUCT WHERE Pro_code = %s", (id, ))
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        precio = float(fila[2]) 
        idCategoria = fila[3]
        unidad = fila[4]
        return f"id: {id_producto} - producto: {nombre} - precio: {precio} - idCategoria: {idCategoria} - unidad: {unidad}" 

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
    consultar_productosSinInventario(db)
    conection = db.cursor()
    producto = pedirIdEntero("Ingrese el ID del producto a actualizar: ")
    if not validar_clave_foranea(db, "PRODUCT", "Pro_Code", producto):
        printMensajeErrorFK()
        return
    
    cat_id = pedirCategoria(db)
    precio = pedirDecimalPositivo("Ingrese el nuevo precio del producto: ")
    unidadMedida = pedirUnidadMedidad("Ingrese la nueva unidad de medida del producto: ")

    query = "UPDATE PRODUCT SET Pro_Price=%s, Cat_ID=%s, Pro_UnitSize=%s WHERE Pro_Code=%s"
    values = (precio, cat_id, unidadMedida, producto)  
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_producto(db):
    consultar_productosSinInventario(db)
    conection = db.cursor()
    producto = pedirIdEntero("Ingrese el ID del producto a actualizar: ")
    if not validar_clave_foranea(db, "PRODUCT", "Pro_Code", producto):
        printMensajeErrorFK()
        return
    
    query = "DELETE FROM PRODUCT WHERE Pro_Code=%s"
    values = (producto, )      
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def CRUD_CategoriaProductos(db):
    while True:
        print(msj.opcionesCategoriaProducto)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_categoriaProducto(db)
        elif opcion == "2":
            mostrarCategorias(db)
        elif opcion == "3":
            actualizar_categoriaProducto(db)
        elif opcion == "4":
            eliminar_categoriaProducto(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)

def insert_categoriaProducto(db):
    nombre = pedirNombreConSignos("Nombre de la Categoría: ")
    conection = db.cursor()
    conection.execute("INSERT INTO CATEGORYPROD (Cat_Name) VALUES (%s)", (nombre, ))
    db.commit()
    printIngresoExitoso()

def actualizar_categoriaProducto(db):
    mostrarCategorias(db)
    conection = db.cursor()
    categoria = pedirIdEntero("Ingrese el ID de la Categoría a actualizar: ")
    if not validar_clave_foranea(db, "CATEGORYPROD", "Cat_ID", categoria):
        printMensajeErrorFK()
        return

    nombre = pedirNombreConSignos("Nombre actualizado de la Categoría: ")
    query = "UPDATE CATEGORYPROD SET Cat_Name=%s WHERE Cat_ID=%s"
    values = (nombre, categoria)  
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_categoriaProducto(db):
    mostrarCategorias(db)
    conection = db.cursor()
    categoria = pedirIdEntero("Ingrese el ID de la Categoría a eliminar: ")
    if not validar_clave_foranea(db, "CATEGORYPROD", "Cat_ID", categoria):
        printMensajeErrorFK()
        return
    
    query = "DELETE FROM CATEGORYPROD WHERE Cat_ID=%s"
    values = (categoria, )      
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def menu_crud_productos(db):
    while True:
        print(msj.opcionesProducto)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_producto(db)
        elif opcion == "2":
            consultar_productosSinInventario(db)
        elif opcion == "3":
            actualizar_producto(db)
        elif opcion == "4":
            eliminar_producto(db)
        elif opcion == "5":
            CRUD_CategoriaProductos(db)
        elif opcion == "6":
            break
        else:
            print(msj.opcionesError)