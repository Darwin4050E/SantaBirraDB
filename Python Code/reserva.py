import mensajes as msj
from clientes import insertar_cliente
from zona import *
from inputHelper import *
from fechaHelper import *
from miembros import *
from promociones import *
from eventos import *
from clientes import *
from outputHelper import *
from validadorFK import *
from prettytable import PrettyTable

def insertar_reserva(db):
    conection = db.cursor()
    fecha = getFecha()
    hora = getHora()
    cliente = pedirCliente(db)
    promotor = pedirPromotor(db)
    promocion = pedirPromocion(db)
    evento = pedirEvento(db)
    estado = pedirEstado(db)
    zona = pedirZona(db)

    tupla = (fecha, hora, cliente, promotor, promocion, evento, estado)

    query = "INSERT INTO BOOKING(Boo_Date, Boo_Hour, Cus_ID, Mem_ID, Prom_ID, Eve_ID, Sta_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    conection.execute(query,tupla)
    db.commit()    

    conection.execute("SELECT LAST_INSERT_ID()")
    ultimo_id = conection.fetchone()[0]

    query = "INSERT INTO BOOKING_ZONE(Boo_ID, Zon_ID) VALUES (%s, %s)"
    conection.execute(query,(ultimo_id, zona))
    db.commit()

    print()
    nro_participantes = pedirEnteroPositivo("Ingrese la cantidad de acompañantes: ")
    if nro_participantes > 0:
        ids_acompanates = lista_acompanantes(nro_participantes)
        registrar_acompanantes(ultimo_id, ids_acompanates, db)
    print("Reserva registrada con éxito.")
    

def pedirPromotor(db):
    opcion = pedirEntreDosOpciones("Opciones para Promotor", "No asignar Promotor", "Ingresar Promotor")
    if opcion == 1:
        return None
    else:
        consultar_empleadosPorRol(db, "PROMOTOR")
        promotor = pedirCedula("Cédula del promotor: ")
        while not validar_clave_foranea(db, "PROMOTOR", "Mem_ID", promotor):
            printMensajeErrorFK()
            promotor = pedirCedula("Cédula del promotor: ")
        return promotor

def pedirPromocion(db):
    opcion = pedirEntreDosOpciones("Opciones para Promoción", "No asignar Promoción", "Ingresar Promoción")
    if opcion == 1:
        return None
    else:
        consultar_promociones(db)
        promocion = pedirIdEntero("ID de la promoción: ")
        while not validar_clave_foranea(db, "PROMOTION", "Prom_ID", promocion):
            printMensajeErrorFK()
            promocion = pedirIdEntero("ID de la promoción: ")   
        return promocion

def pedirEvento(db):
    print("\nEventos:")
    consultar_eventos(db)
    evento = pedirIdEntero("ID del evento: ")
    while not validar_clave_foranea(db, "EVENT", "Eve_ID", evento):
        printMensajeErrorFK()
        evento = pedirIdEntero("ID del evento: ")     
    return evento

def pedirCliente(db):
    print("\nClientes:")
    consultar_clientes(db)
    cliente = pedirCedula("Cédula del cliente: ")
    while not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", cliente):
        printMensajeErrorFK()
        cliente = pedirCedula("Cédula del cliente: ")
    return cliente

def pedirEstado(db):
    print("\nEstados:")
    consultar_estados(db)
    estado = pedirIdEntero("ID del estado: ")
    while not validar_clave_foranea(db, "STATUS", "Sta_ID", estado):
        printMensajeErrorFK()
        estado = pedirIdEntero("ID del estado: ")
    return estado

def consultar_estados(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM STATUS")
    datos = conection.fetchall()
    for fila in datos:
        print(f"ID: {fila[0]} - Nombre: {fila[1]}")

def pedirZona(db):
    print("\nZonas:")
    consultar_zonas(db)
    zona = pedirIdEntero("ID de la zona: ")
    while not validar_clave_foranea(db, "ZONE", "Zon_ID", zona):
        printMensajeErrorFK()
        zona = pedirIdEntero("ID de la zona: ")
    return zona

def validar_y_registrar_clientes(ids_clientes, db):
    conection = db.cursor()
    query = "SELECT Cus_ID FROM CUSTOMER WHERE Cus_ID in (%s)" % ','.join(['%s']*len(ids_clientes))
    conection.execute(query, ids_clientes)
    datos = conection.fetchall()

    ids_validos = {fila[0] for fila in datos}

    ids_invalidos = set(ids_clientes) - ids_validos

    for id_invalido in ids_invalidos:
        print()
        print(f"El cliente con ID {id_invalido} no existe.")
        print("Por favor, ingrese los datos del cliente.")
        insertar_cliente(db)

def lista_acompanantes(db, nro_acompanantes):
    print("\nClientes disponibles:")
    consultar_clientes(db)
    lista = []
    for i in range(nro_acompanantes):
        id_acompanante = pedirCedula(f"Ingrese la cédula del acompañante {i+1}: ")
        lista.append(id_acompanante)
    return lista

def registrar_acompanantes(id_reserva, ids_acompanantes, db):
    conection = db.cursor()
    validar_y_registrar_clientes(ids_acompanantes, db)
    for id_acompanante in ids_acompanantes:
        query = "INSERT INTO BOOKING_CUSTOMER(Boo_ID, Cus_ID) VALUES (%s, %s)"
        conection.execute(query, (id_reserva, id_acompanante))
        db.commit()
    print("Acompañantes registrados con éxito.")

def consultar_datos_reserva(db, reserva):
    conection = db.cursor()
    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", reserva):
        printMensajeErrorFK()
        return
    
    conection.execute("SELECT * FROM BOOKING JOIN BOOKING_CUSTOMER USING (Boo_ID) WHERE Boo_ID = %s", (reserva,))
    datos = conection.fetchall()
    print("\nDatos de la reserva:")
    if len(datos) == 0:
        print("No se encontraron acompañantes.")
        return
    
    tabla = PrettyTable()
    tabla.field_names = ["ID Reserva", "Fecha", "Hora", "ID Cliente", "ID Promotor", "ID Promoción", "ID Evento", "ID Estado", "Acompañante"]
    for fila in datos:
        id_reserva = fila[0]
        fecha = fila[1]
        hora = fila[2]
        cliente_id = fila[3]
        promotor_id = fila[4]
        promocion_id = fila[5]
        evento_id = fila[6]
        estado_id = fila[7]
        acompañante = fila[8]
        tabla.add_row([id_reserva, fecha, hora, cliente_id, promotor_id, promocion_id, evento_id, estado_id, acompañante])
    print(tabla)
    
def consultar_reserva(db, reserva):
    conection = db.cursor()
    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", reserva):
        printMensajeErrorFK()
        return
    
    conection.execute("SELECT * FROM BOOKING WHERE Boo_ID = %s", (reserva,))
    tabla = PrettyTable()
    tabla.field_names = ["ID Reserva", "Fecha", "Hora", "ID Cliente", "ID Promotor", "ID Promoción", "ID Evento", "ID Estado"]

    datos = conection.fetchall()
    for fila in datos:
        id_reserva = fila[0]
        fecha = fila[1]
        hora = fila[2]
        cliente_id = fila[3]
        promotor_id = fila[4]
        promocion_id = fila[5]
        evento_id = fila[6]
        estado_id = fila[7]
        tabla.add_row([id_reserva, fecha, hora, cliente_id, promotor_id, promocion_id, evento_id, estado_id])
    print(tabla)

def consultar_reservas(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM BOOKING")
    tabla = PrettyTable()
    tabla.field_names = ["ID Reserva", "Fecha", "Hora", "ID Cliente", "ID Promotor", "ID Promoción", "ID Evento", "ID Estado"]
    datos = conection.fetchall()
    for fila in datos:
        id_reserva = fila[0]
        fecha = fila[1]
        hora = fila[2]
        cliente_id = fila[3]
        promotor_id = fila[4]
        promocion_id = fila[5]
        evento_id = fila[6]
        estado_id = fila[7]
        tabla.add_row([id_reserva, fecha, hora, cliente_id, promotor_id, promocion_id, evento_id, estado_id])
    print(tabla)

def pedirIdReserva(db):
    consultar_reservas(db)
    print()
    id_reserva = pedirIdEntero("Ingrese el ID de la reserva: ")
    while not validar_clave_foranea(db, "BOOKING", "Boo_ID", id_reserva):
        printMensajeErrorFK()
        id_reserva = pedirIdEntero("Ingrese el ID de la reserva: ")
    return id_reserva

def actualizar_reserva(db, reserva_id):
    conection = db.cursor()
    
    consultar_reserva(db, reserva_id)

    while True:
        print(msj.opcionesActualizacionReserva)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            actualizar_fecha(conection,reserva_id,db)
        elif opcion == "2":
            actualizar_hora(conection,reserva_id,db)
        elif opcion == "3":
            actualizar_zona(conection,reserva_id,db)
        elif opcion == "4":
            actualizar_estado(conection,reserva_id,db)
        elif opcion == "5":
            actualizar_promocion(conection,reserva_id,db)
        elif opcion == "6":
            break
        else:
            print(msj.opcionesError)

def actualizar_fecha(conection,reserva_id,db):
    fecha = getFecha()
    query = "UPDATE BOOKING SET Boo_Date=%s WHERE Boo_ID=%s"
    values = (fecha, reserva_id)
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def actualizar_hora(conection,reserva_id,db):
    hora = getHora()
    query = "UPDATE BOOKING SET Boo_Hour=%s WHERE Boo_ID=%s"
    values = (hora, reserva_id)
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def actualizar_zona(conection, reserva_id,db):
    zona = pedirZona(db)
    query = "UPDATE BOOKING_ZONE SET Zon_ID=%s WHERE Boo_ID=%s"
    values = (zona, reserva_id)
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def actualizar_estado(conection, reserva_id,db):
    estado = pedirEstado(db)
    query = "UPDATE BOOKING SET Sta_ID=%s WHERE Boo_ID=%s"
    values = (estado, reserva_id)
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def actualizar_promocion(conection, reserva_id, db):
    promocion = pedirPromocion(db)
    query = "UPDATE BOOKING SET Prom_ID=%s WHERE Boo_ID=%s"
    values = (promocion, reserva_id)
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_reserva(db, reserva):
    conection = db.cursor()
    query = "DELETE FROM BOOKING WHERE Boo_ID=%s"
    values = (reserva,)
    conection.execute(query, values)
    db.commit()
    
    if conection.rowcount == 0:
        printMensajeErrorFK()
    else:
        printEliminacionExitosa()


def menu_crud_reservas(db):
    while True:
        print(msj.opcionesReserva)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insertar_reserva(db)
        elif opcion == "2":
            consultar_reservas(db)
        elif opcion == "3":
            reserva = pedirIdReserva(db)
            consultar_datos_reserva(db, reserva)
        elif opcion == "4":
            reserva = pedirIdReserva(db)
            actualizar_reserva(db, reserva)
        elif opcion == "5":
            reserva = pedirIdReserva(db)
            eliminar_reserva(db, reserva)
        elif opcion == "6":
            break
        else:
            print(msj.opcionesError)