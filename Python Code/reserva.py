def insertar_reserva(db):
    conection = db.cursor()
    fecha = input("Por favor ingresa la fecha de la reserva (YYYY-MM-DD): ")
    hora = input("Por favor ingresa la hora de la reserva (HH:mm:ss): ")
    cliente = input("Ingrese el ID del cliente que realizó la reserva: ")
    promotor = input("Por favor ingrese el ID del promotor del evento: ")
    promocion = input("Por favor ingrese el ID de la promoción: ")
    evento = input("Por favor ingrese el ID del evento: ")
    estado = input("Por favor ingrese el ID de estado de la reserva: ")
    tupla = (fecha, hora, cliente, promotor,promocion, evento, estado)

    query = "INSERT INTO BOOKING(Boo_Date, Boo_Hour, Cus_ID, Mem_ID, Prom_ID, Eve_ID, Sta_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    conection.execute(query,tupla)
    db.commit()
    print("Reserva ingresada con éxito.")

def consultar_reserva(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM BOOKING")
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
        print(f"(Num. Reserva: {id_reserva}, Fecha: {fecha}, Hora: {hora}, ID Cliente: {cliente_id}, ID Promotor: {promotor_id}, ID Promocion: {promocion_id}, ID Evento: {evento_id}, ID Estado: {estado_id})")

def actualizar_reserva(db):
    print(":D")

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

def menu_crud_reserva(db):
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