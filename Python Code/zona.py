import mensajes as msj
from inputHelper import *
from outputHelper import *
from miembros import *
from validadorFK import *
from prettytable import PrettyTable


def insertar_zona(db):
    conection = db.cursor()
    nombre = pedirNombreEmpresa("Ingrese el nombre de la zona: ")
    capacidad = pedirNatural("Ingrese la capacidad de la zona: ")
    guardia = pedirGuardia(db)
    query = "INSERT INTO ZONE (Zon_Capacity, Mem_ID, Zon_Name) VALUES (%s, %s, %s)"
    values = (capacidad, guardia, nombre)
    conection.execute(query, values)
    db.commit()
    printIngresoExitoso()

def pedirGuardia(db):
    opcion = pedirEntreDosOpciones("Opciones para Guardia", "No asignar Guardia", "Ingresar Guardia")
    if opcion == 1:
        return None
    else:
        consultar_empleadosPorRol(db, "GUARD")
        manager = pedirCedula("Cédula del guardia: ")
        while not validar_clave_foranea(db, "GUARD", "Mem_ID", manager):
            printMensajeErrorFK()
            manager = pedirCedula("Cédula del guardia: ")
        return manager

def consultar_zonas(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM ZONE")
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Capacidad", "Guardia", "Nombre", "Recargo VIP"]
    datos = conection.fetchall()
    for fila in datos:
        if fila[0] == 1:
            recargo = consultar_recargoVIP(db)
            id_zona = fila[0]
            capacidad = fila[1]
            codGuardia = fila[2]
            nombre = fila[3]
            tabla.add_row([id_zona, capacidad, codGuardia, nombre, recargo])
        else:
            id_zona = fila[0]
            capacidad = fila[1]
            codGuardia = fila[2]
            nombre = fila[3]
            tabla.add_row([id_zona, capacidad, codGuardia, nombre, "N/A"])
    print(tabla)
    
def consultar_recargoVIP(db):
    conection = db.cursor()
    conection.execute("SELECT Charge_VIP FROM ZoneVIP WHERE Zon_ID=1")
    datos = conection.fetchone()
    recargo = datos[0]
    return recargo

def actualizar_zonaVIP(db):
    conection = db.cursor()
    recargo = pedirDecimalPositivo("Ingrese el recargo VIP: ")
    query = "UPDATE ZoneVIP SET Charge_VIP=%s WHERE Zon_ID=1"
    values = (recargo, )
    conection.execute(query, values)
    db.commit()

def actualizar_zona(db): 
    conection = db.cursor()
    idZona = pedirIdEntero("Ingrese el ID de la zona a actualizar: ")

    if not validar_clave_foranea(db, "ZONE", "Zon_ID", idZona):
        printMensajeErrorFK()
        return
    
    nombre = pedirNombreEmpresa("Ingrese el nuevo nombre de la zona: ")
    capacidad = pedirNatural("Ingrese la nueva capacidad: ")
    guardia = pedirGuardia(db)

    query = "UPDATE ZONE SET Zon_Capacity=%s, Mem_ID=%s, Zon_Name=%s WHERE Zon_ID=%s"    
    values = (capacidad, guardia, nombre, idZona)
    conection.execute(query, values)
    db.commit()

    if idZona == 1:
        actualizar_zonaVIP(db)

    printActualizacionExitosa()

def eliminar_zona(db):
    conection = db.cursor()
    idZona = pedirIdEntero("Ingrese el ID de la zona a eliminar: ")

    if not validar_clave_foranea(db, "ZONE", "Zon_ID", idZona):
        printMensajeErrorFK()
        return
    
    query = "DELETE FROM ZONE WHERE Zon_ID=%s"    
    values = (idZona, )
    conection.execute(query, values)
    db.commit()


def menu_crud_zonas(db):
    while True:
        print(msj.opcionesZona)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insertar_zona(db)
        elif opcion == "2":
            consultar_zonas(db)
        elif opcion == "3":
            consultar_zonas(db)
            actualizar_zona(db)
        elif opcion == "4":
            consultar_zonas(db)
            eliminar_zona(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)