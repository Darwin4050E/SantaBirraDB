from validadorFK import *
from datetime import *
import mensajes as msj
from inputHelper import *
from fechaHelper import *
from outputHelper import *
from miembros import *
from clientes import *
from prettytable import PrettyTable

def insert_incidente(db):
    conection = db.cursor()
    descripcion = pedirDescripcion("Descripción del incidente: ")
    
    guardia = pedirGuardia(db, "Cédula del guardia encargado: ")

    if not validar_clave_foranea(db, "GUARD", "Mem_ID", guardia):
        printMensajeErrorFK()
        return

    tupla = (descripcion, guardia)
    sql = "INSERT INTO INCIDENT (Inc_Desc, Mem_ID) VALUES (%s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()
    conection.close()

def pedirGuardia(db, mensaje):
    print("\nGuardias disponibles: ")
    consultar_empleadosPorRol(db, "GUARD")
    guardia = pedirCedula(mensaje)
    return guardia

def agregar_clientes_incidente(db):
    idIncidente = pedirIdEntero("ID del incidente: ")

    if not validar_clave_foranea(db, "INCIDENT", "Inc_ID", idIncidente):
        printMensajeErrorFK()
        return
    
    fecha = getFecha()
    cantidad = pedirNatural("Cantidad de clientes a agregar: ")
    
    consultar_clientes(db)
    for i in range(cantidad):
        idCliente = pedirCedula(f"ID del cliente {i+1} : ")
        if not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", idCliente):
            printMensajeErrorAgregacion()
        else:
            cliente_incidente(db, idIncidente, idCliente, fecha)

def existe_clienteEnIncidente(db, idIncidente, idCliente):
    conection = db.cursor()
    query = "SELECT COUNT(*) FROM INCIDENT_CUSTOMER WHERE Inc_ID = %s AND Cus_ID = %s"
    conection.execute(query, (idIncidente, idCliente))
    return conection.fetchone()[0] > 0

#Saca el último ID artifical de la combinación incidente - cliente
def ultimo_IDIncCustomer(db, idIncidente, idCliente):
    conection = db.cursor()
    if existe_clienteEnIncidente(db, idIncidente, idCliente):
        query = "SELECT IC_ID FROM INCIDENT_CUSTOMER WHERE Inc_ID = %s AND Cus_ID = %s ORDER BY IC_ID DESC LIMIT 1"
        tupla = (idIncidente, idCliente)
        conection.execute(query, tupla)
        ic_id = conection.fetchone()
        return int(ic_id[0])
    else:
        return 0

def cliente_incidente(db, idIncidente, idCliente, fecha):
    conection = db.cursor()
    ic_id = ultimo_IDIncCustomer(db,idIncidente, idCliente) + 1
    tupla = (ic_id, idIncidente, idCliente, fecha)
    sql = "INSERT INTO INCIDENT_CUSTOMER (IC_ID, Inc_ID, Cus_ID, Inc_Date) VALUES (%s, %s, %s, %s)"
    conection.execute(sql,tupla)
    db.commit()
    print("Cliente agregado al incidente.")

def consultar_incidentes(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INCIDENT NATURAL JOIN INCIDENT_CUSTOMER ORDER BY INC_DATE DESC")
    datos = conection.fetchall()
    tabla = PrettyTable()
    tabla.field_names = ["ID Incidente", "Descripción", "Guardia", "ID I-C", "Cliente", "Fecha"]
    for fila in datos:
        id = fila[0]
        descripcion = fila[1]
        guardia = fila[2]
        ic_id = fila[3]
        cliente = fila[4]
        fecha = fila[5].strftime("%d/%m/%Y")
        tabla.add_row([id, descripcion, guardia, ic_id, cliente, fecha])
    print(tabla)
        
def consultar_tipos_incidente(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INCIDENT")
    datos = conection.fetchall()
    tabla = PrettyTable()
    tabla.field_names = ["ID", "Descripción", "Guardia"]

    for fila in datos:
        id = fila[0]
        descripcion = fila[1]
        guardia = fila[2]
        tabla.add_row([id, descripcion, guardia])
    print(tabla)
    
def actualizar_incidente(db):
    conection = db.cursor()
    codIncidente = pedirIdEntero("ID del incidente: ")
    if not validar_clave_foranea(db, "INCIDENT", "Inc_ID", codIncidente):
        printMensajeErrorFK()
        return

    guardia = pedirGuardia(db, "Cédula actualizada del guardia encargado: ")

    if not validar_clave_foranea(db, "GUARD", "Mem_ID", guardia):
        printMensajeErrorFK()
        return

    descripcion = pedirDescripcion("Descripción del incidente actualizada: ")

    query = "UPDATE INCIDENT SET Inc_Desc=%s, Mem_ID=%s WHERE Inc_ID = %s"
    values = (descripcion, guardia, codIncidente)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_incidente(db):
    conection = db.cursor()
    codIncidente = pedirIdEntero("ID del incidente: ")    
    query = "DELETE FROM INCIDENT WHERE Inc_ID = %s"
    values = (codIncidente, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        printMensajeErrorFK()
    else:
        printEliminacionExitosa()

def eliminarClienteDeIncidente(db):
    conection = db.cursor()
    codIncidente = pedirIdEntero("ID del incidente: ")
    if not validar_clave_foranea(db, "INCIDENT", "Inc_ID", codIncidente):
        printMensajeErrorFK()
        return
    
    idCliente = pedirCedula("ID del cliente: ")
    if not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", idCliente):
        printMensajeErrorFK()
        return
    
    ic_id = pedirIdEntero("ID de la relación incidente-cliente: ")

    query = "DELETE FROM INCIDENT_CUSTOMER WHERE Inc_ID = %s AND Cus_ID = %s AND IC_ID = %s"
    values = (codIncidente, idCliente, ic_id)

    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        printMensajeErrorFK()
    else:
        printEliminacionExitosa()

def menu_crud_incidentes(db):
    while True:
        print(msj.opcionesIncidentes)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_incidente(db)
        elif opcion == "2":
            consultar_tipos_incidente(db)
            agregar_clientes_incidente(db)
        elif opcion == "3": 
            consultar_tipos_incidente(db)
        elif opcion == "4":
            consultar_incidentes(db)
        elif opcion == "5":
            consultar_tipos_incidente(db)
            actualizar_incidente(db)
        elif opcion == "6":
            consultar_tipos_incidente(db)
            eliminar_incidente(db)
        elif opcion == "7":
            consultar_incidentes(db)
            eliminarClienteDeIncidente(db) 
        elif opcion == "8":
            break
        else:
            print(msj.opcionesError)