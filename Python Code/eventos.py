import mensajes as msj
import inventario
from inputHelper import *
from outputHelper import *
from fechaHelper import *
from validadorFK import *

def insertar_Evento(db):
    mostrarCategorias(db)
    cat_id = pedirIdEntero("ID de la categoría: ")
    if not validar_clave_foranea(db, "CATEGORYEVE", "Cat_ID", cat_id):
        printMensajeErrorFK()
        return
    
    nombre = pedirNombreConSignos("Nombre del Evento: ")
    precioHombres = pedirDecimalPositivo("Precio para Hombres: ")
    precioMujeres = pedirDecimalPositivo("Precio para Mujeres: ")

    conection = db.cursor()
    tupla = (nombre, precioHombres, precioMujeres, cat_id)
    sql = "INSERT INTO EVENT (Eve_Name, Eve_PMan, Eve_PWoman, Cat_ID) VALUES (%s, %s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def mostrarCategorias(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM CATEGORYEVE")
    datos = conection.fetchall()
    for fila in datos:
        id_producto = fila[0]
        nombre = fila[1]
        print(f"id: {id_producto} - categoria: {nombre}") 

def pedirCategoria(db):
    mostrarCategorias(db)
    cat_id = pedirIdEntero("ID de la categoría actual: ")
    while not validar_clave_foranea(db, "CATEGORYEVE", "Cat_ID", cat_id):
        printMensajeErrorFK()
        cat_id = pedirIdEntero("ID de la categoría actual: ")
    return cat_id

def consultar_eventos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM EVENT NATURAL JOIN CATEGORYEVE")
    datos = conection.fetchall()
    for fila in datos:
        id_categoria = fila[0]
        id_evento = fila[1]
        nombre = fila[2]
        precioH = fila[3]
        precioM = fila[4]
        categoria = fila[5]
        print(f"id: {id_evento} - nombre: {nombre} - precioH: {precioH} - precioM: {precioM} - id_cat: {id_categoria} -categoria: {categoria}") 

def actualizar_eventos(db):
    consultar_eventos(db)
    conection = db.cursor()
    evento = pedirIdEntero("Ingrese el ID del Evento a actualizar: ")
    if not validar_clave_foranea(db, "EVENT", "Eve_ID", evento):
        printMensajeErrorFK()
        return

    categoria = pedirCategoria(db)
    nombre = pedirNombreConSignos("Nombre actualizado del Evento: ")
    precioHombres = pedirDecimalPositivo("Precio actualizado para Hombres: ")
    precioMujeres = pedirDecimalPositivo("Precio actualizado para Mujeres: ")

    query = "UPDATE EVENT SET Eve_Name=%s, Eve_PMan=%s, Eve_PWoman=%s, Cat_ID=%s WHERE Eve_ID=%s"
    values = (nombre, precioHombres, precioMujeres, categoria, evento)  
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_evento(db):
    consultar_eventos(db)
    conection = db.cursor()
    evento = pedirIdEntero("Ingrese el ID del Evento a actualizar: ")
    if not validar_clave_foranea(db, "EVENT", "Eve_ID", evento):
        printMensajeErrorFK()
        return
    
    query = "DELETE FROM EVENT WHERE Eve_ID=%s"
    values = (evento, )      
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def CRUD_CategoriaEvento(db):
    while True:
        print(msj.opcionesCategoriaEvento)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insertar_categoriaEve(db)
        elif opcion == "2":
            mostrarCategorias(db)
        elif opcion == "3":
            actualizar_categoriasEve(db)
        elif opcion == "4":
            eliminar_cateogriasEve(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)

def insertar_categoriaEve(db):
    nombre = pedirNombreConSignos("Nombre de la Categoría: ")
    conection = db.cursor()
    tupla = (nombre,)
    sql = "INSERT INTO CATEGORYEVE (Cat_Name) VALUES (%s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def actualizar_categoriasEve(db):
    mostrarCategorias(db)
    conection = db.cursor()
    categoria = pedirIdEntero("Ingrese el ID de la Categoría a actualizar: ")
    if not validar_clave_foranea(db, "CATEGORYEVE", "Cat_ID", categoria):
        printMensajeErrorFK()
        return

    nombre = pedirNombreConSignos("Nombre actualizado de la Categoría: ")
    query = "UPDATE CATEGORYEVE SET Cat_Name=%s WHERE Cat_ID=%s"
    values = (nombre, categoria)  
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_cateogriasEve(db):
    mostrarCategorias(db)
    conection = db.cursor()
    categoria = pedirIdEntero("Ingrese el ID de la Categoría a eliminar: ")
    if not validar_clave_foranea(db, "CATEGORYEVE", "Cat_ID", categoria):
        printMensajeErrorFK()
        return
    
    query = "DELETE FROM CATEGORYEVE WHERE Cat_ID=%s"
    values = (categoria, )      
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()


def menu_crud_eventos(db):
    while True:
        print(msj.opcionesEvento)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insertar_Evento(db)
        elif opcion == "2":
            consultar_eventos(db)
        elif opcion == "3":
            actualizar_eventos(db)
        elif opcion == "4":
            eliminar_evento(db)
        elif opcion == "5":
            CRUD_CategoriaEvento(db)
        elif opcion == "6":
            break
        else:
            print(msj.opcionesError)