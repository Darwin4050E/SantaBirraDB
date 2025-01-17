from validadorFK import *
from datetime import *
import mensajes as msj
from inputHelper import *
from outputHelper import *
from fechaHelper import *
from zona import *
from prettytable import PrettyTable

def insert_object(db):
    conection = db.cursor()
    
    descripcion = pedirDescripcion("Descripción del objeto: ")
    fecha = getFecha()
    codZona = pedirZona(db)

    tupla = (fecha, descripcion, codZona)
    sql = "INSERT INTO LOSTOBJECT (Los_Date, Los_Des, Zon_ID) VALUES (%s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def pedirZona(db):
    opcion = pedirEntreDosOpciones("Opciones para Zona", "No asignar Zona", "Ingresar Zona")
    if opcion == 1:
        return None
    else:
        consultar_zonas(db)
        zona = pedirIdEntero("ID de la zona: ")
        while not validar_clave_foranea(db, "Zone", "Zon_ID", zona):
            printMensajeErrorFK()
            zona = pedirIdEntero("ID de la zona: ")
        return zona

def consultar_objetos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM LOSTOBJECT")
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Fecha", "Descripción", "Zona"]
    datos = conection.fetchall()
    for fila in datos:
        id = fila[0]
        fecha = fila[1].strftime("%d/%m/%Y")
        descripcion = fila[2]
        zona = fila[3]
        tabla.add_row([id, fecha, descripcion, zona])
    print(tabla)
    
def actualizar_objeto(db):
    consultar_objetos(db)
    conection = db.cursor()
    codObjeto = pedirIdEntero("ID del objeto perdido: ")

    if not validar_clave_foranea(db, "LOSTOBJECT", "Los_ID", codObjeto):
        printMensajeErrorFK()
        return

    descripcion = pedirDescripcion("Descripción del objeto: ")
    fecha = getFecha()
    zona = pedirZona(db)

    query = "UPDATE LOSTOBJECT SET Los_Date=%s, Los_Des=%s, Zon_ID=%s WHERE Los_ID=%s"
    values = (fecha, descripcion, zona, codObjeto)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_objeto(db):
    consultar_objetos(db)
    conection = db.cursor()
    codObjeto = pedirIdEntero("ID del objeto perdido: ")

    if not validar_clave_foranea(db, "LOSTOBJECT", "Los_ID", codObjeto):
        printMensajeErrorFK()
        return

    query = "DELETE FROM LOSTOBJECT WHERE Los_ID=%s"
    values = (codObjeto, )
            
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def menu_crud_objetosperdidos(db):
    while True:
        print(msj.opcionesObjetoPerdido)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_object(db)
        elif opcion == "2":
            consultar_objetos(db)
        elif opcion == "3":
            actualizar_objeto(db)
        elif opcion == "4":
            eliminar_objeto(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)