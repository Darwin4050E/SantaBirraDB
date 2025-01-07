from validadorFK import *
from datetime import *
import mensajes as msj

def insert_incidente(db):
    conection = db.cursor()
    descripcion = input("Descripción del incidente: ")
    guardia = input("ID del guardia que atendió el incidente: ")

    if not validar_clave_foranea(db, "GUARD", "Mem_ID", guardia):
        print("No existe guardia con ese ID")
        return

    tupla = (descripcion, guardia)
    sql = "INSERT INTO INCIDENT (Inc_Desc, Mem_ID) VALUES (%s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    print("Incidente agregado con éxito.")

def agregar_clientes_incidente(db):
    conection = db.cursor()
    idIncidente = input("Ingrese el ID del incidente: ")

    if not validar_clave_foranea(db, "INCIDENT", "Inc_ID", idIncidente):
        print("No existe incidente con ese ID")
        return
    
    cantidad = int(input("Ingrese la cantidad de clientes que participaron en el incidente: "))
    if cantidad <= 0:
        print("Ingrese datos válidos.")
        return
    
    fechaIngresada = input("Fecha del incidente (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()
    
    for i in range(cantidad):
        idCliente = input("Ingrese ID del cliente: ")
        if not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", idCliente):
            print("No existe tal cliente. Por favor agreguelo en la sección de clientes e intente de nuevo.")
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
    for fila in datos:
        id = fila[0]
        descripcion = fila[1]
        guardia = fila[2]
        ic_id = fila[3]
        cliente = fila[4]
        fecha = fila[5].strftime("%d/%m/%Y")
        print(f"id: {id} - descripcion: {descripcion} - guardia: {guardia} - IC_ID: {ic_id} - cliente: {cliente} - fecha: {fecha}")
        
def consultar_tipos_incidente(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INCIDENT")
    datos = conection.fetchall()
    for fila in datos:
        id = fila[0]
        descripcion = fila[1]
        guardia = fila[2]
        print(f"id: {id} - descripcion: {descripcion} - guardia: {guardia}")

def actualizar_incidente(db):
    conection = db.cursor()
    codIncidente = input("ID del incidente: ")
    guardia = input("ID del guardia que atendió el incidente actualizado: ")

    if not validar_clave_foranea(db, "GUARD", "Mem_ID", guardia):
        print("No existe guardia con ese ID.")
        return

    descripcion = input("Descripción actualizada: ")

    query = "UPDATE INCIDENT SET Inc_Desc=%s, Mem_ID=%s WHERE Inc_ID = %s"
    values = (descripcion, guardia, codIncidente)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal incidente.")
    else:
        print(f"Incidente Actualizado.")

def eliminar_incidente(db):
    conection = db.cursor()
    codIncidente = input("ID del incidente: ")
    
    query = "DELETE FROM INCIDENT WHERE Inc_ID = %s"
    values = (codIncidente, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal incidente.")
    else:
        print(f"Incidente eliminado.")

def eliminarClienteDeIncidente(db):
    conection = db.cursor()
    codIncidente = input("ID del incidente: ")
    if not validar_clave_foranea(db, "INCIDENT", "Inc_ID", codIncidente):
        print("No existe incidente con ese ID")
        return
    
    idCliente = input("ID del cliente: ")
    if not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", idCliente):
        print("No existe tal cliente.")
        return
    
    ic_id = input("Ingrese el ID de dicha combinación Incidente-Cliente: ")

    query = "DELETE FROM INCIDENT_CUSTOMER WHERE Inc_ID = %s AND Cus_ID = %s AND IC_ID = %s"
    values = (codIncidente, idCliente, ic_id)

    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal registro de incidente.")
    else:
        print(f"Cliente eliminado de dicho incidente.")

def menu_crud_incidentes(db):
    while True:
        print(msj.opcionesIncidentes)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_incidente(db)
        elif opcion == "2":
            agregar_clientes_incidente(db)
        elif opcion == "3": 
            consultar_tipos_incidente(db)
        elif opcion == "4":
            consultar_incidentes(db)
        elif opcion == "5":
            actualizar_incidente(db)
        elif opcion == "6":
            eliminar_incidente(db)
        elif opcion == "7":
            eliminarClienteDeIncidente(db) 
        elif opcion == "8":
            break
        else:
            print(msj.opcionesError)