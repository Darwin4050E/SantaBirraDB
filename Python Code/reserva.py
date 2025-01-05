from clientes import insertar_cliente

def insertar_reserva(db):
    conection = db.cursor()
    fechaIngresada = input("Por favor ingresa la fecha de la reserva (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%D").date()
    horaIngresada = input("Por favor ingresa la hora de la reserva (HH:mm:ss): ")
    hora = datetime.strptime(horaIngresada, "%H:%M:%S").time()
    cliente = input("Ingrese el ID del cliente que realizó la reserva: ")
    promotor = input("Por favor ingrese el ID del promotor del evento: ")
    promocion = input("Por favor ingrese el ID de la promoción: ")
    evento = input("Por favor ingrese el ID del evento: ")
    estado = input("Por favor ingrese el ID de estado de la reserva: ")
    tupla = (fecha, hora, cliente, promotor,promocion, evento, estado)

    query = "INSERT INTO BOOKING(Boo_Date, Boo_Hour, Cus_ID, Mem_ID, Prom_ID, Eve_ID, Sta_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    conection.execute(query,tupla)
    db.commit()
    nro_participantes = input("Ingrese el numero de acompañantes: ")
    if nro_participantes > 0:
        ids_acompanates = lista_acompanantes(nro_participantes)
        conection.execute("SELECT LAST_INSERT_ID()")
        ultimo_id = conection.fetchone()[0]
        registrar_acompanantes(ultimo_id, ids_acompanates, db)

    print("Reserva ingresada con éxito.")



def validar_y_registrar_clientes(ids_clientes, db):
    conection = db.cursor()
    query = "SELECT Cus_ID FROM CUSTOMER WHERE Cus_ID in (%s)" % ','.join(['%s']*len(ids_clientes))
    conection.execute(query, ids_clientes)
    datos = conection.fetchall()

    ids_validos = {fila[0] for fila in datos}

    ids_invalidos = set(ids_clientes) - ids_validos

    for id_invalido in ids_invalidos:
        print(f"El cliente con ID {id_invalido} no existe.")
        print("Por favor, ingrese los datos del cliente.")
        insertar_cliente(db)
    
    return True

def validar_ID(id_cliente):
    if id_cliente != 10:
        print("El ID del cliente no es válido. Debe tener 10 caracteres. Intente nuevamente")
        return False
    return True

def lista_acompanantes(nro_acompanantes):
    lista = []
    for i in range(nro_acompanantes):
        while True:
            id_acompanante = input(f"Ingrese el ID del acompañante {i+1}: ")
            if validar_ID(id_acompanante):
                break
        lista.append(id_acompanante)
    return lista

def registrar_acompanantes(id_reserva, ids_acompanantes, db):
    conection = db.cursor()
    if validar_y_registrar_clientes(ids_acompanantes, db):
        for id_acompanante in ids_acompanantes:
            query = "INSERT INTO BOOKING_CUSTOMER(Boo_ID, Cus_ID) VALUES (%s, %s)"
            conection.execute(query, (id_reserva, id_acompanante))
        conection.commit()
        print("Acompañantes registrados con éxito.")

def consultar_reserva(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM BOOKING")
    datos = conection.fetchall()
    for fila in datos:
        id_reserva = fila[0]
        fecha = fila[1].strftime("%Y/%m/%D")
        hora = fila[2].strftime("%H:%M:%S")
        cliente_id = fila[3]
        promotor_id = fila[4]
        promocion_id = fila[5]
        evento_id = fila[6]
        estado_id = fila[7]
        print(f"(Num. Reserva: {id_reserva}, Fecha: {fecha}, Hora: {hora}, ID Cliente: {cliente_id}, ID Promotor: {promotor_id}, ID Promocion: {promocion_id}, ID Evento: {evento_id}, ID Estado: {estado_id})")

def actualizar_reserva(db):
    conection = db.cursor()
    reserva_id = input("Ingrese el ID de la reserva que desea modificar: ")


def eliminar_reserva(db):
    conection = db.cursor()
    reserva_id = input("Ingrese el ID de la reserva que desea eliminar: ")

    query = "DELETE FROM BOOKING WHERE Boo_ID=%s"
    values = (reserva_id, )
    conection.execute(query, values)

    query2 = "DELETE FROM PAY WHERE Boo_ID=%s"
    conection.execute(query2, values)

    query3 = "DELETE FROM BOOKING_CUSTOMER WHERE Boo_ID=%s"
    conection.execute(query3, values)

    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ninguna reserva con ese ID.")
    else:
        print(f"Reserva eliminada.")

def menu_crud_reservas(db):
    while True:
        print("""
        === Gestión de Reservas - Santa Birra ===
        1. Insertar Reserva
        2. Consultar Reserva
        3. Modificar Reserva
        4. Eliminar Reserva
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insertar_reserva(db)
        elif opcion == "2":
            consultar_reserva(db)
        elif opcion == "3":
            actualizar_reserva(db)
        elif opcion == "4":
            eliminar_reserva(db)
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")