from validadorFK import *
from datetime import *
import mensajes as msj

def insert_pago(db):
    conection = db.cursor()
    codReserva = input("ID de la Reserva: ")
    codPago = input("ID del pago: ")

    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", codReserva):
        print("No existe reserva con ese ID")
        return
    if existe_pago(db, codPago, codReserva):
        print("Ya existe pago con el mismo ID para tal reserva.")
        return
    
    fechaIngresada = input("Fecha del pago (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()
    monto = input("Ingrese el monto: ")

    tupla = (codPago, codReserva,  fecha, monto)
    sql = "INSERT INTO PAY (Pay_ID, Boo_ID, Pay_Date, Pay_Amount) VALUES (%s, %s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    print("Pago agregado con éxito.")

def existe_pago(db, codPago, codReserva):
    conection = db.cursor()
    query = f"SELECT COUNT(*) FROM PAY WHERE Pay_ID = %s AND Boo_ID = %s"
    conection.execute(query, (codPago, codReserva))
    return conection.fetchone()[0] > 0

def consultar_pagos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PAY ORDER BY Boo_ID ASC")
    datos = conection.fetchall()
    for fila in datos:
        id = fila[0]
        reservaId = fila[1]
        fecha = fila[2].strftime("%d/%m/%Y")
        monto = fila[3]
        print(f"id: {id} - Id Reserva: {reservaId} - fecha: {fecha} - monto: {monto}")

def actualizar_pago(db):
    conection = db.cursor()
    codReserva = input("ID de la Reserva: ")
    codPago = input("Ingrese el ID del pago: ")

    fechaIngresada = input("Fecha del pago actualizada (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()

    monto = input("Monto actualizado: ")

    query = "UPDATE PAY SET Pay_Date=%s, Pay_Amount=%s WHERE Pay_ID = %s AND Boo_ID=%s"
    values = (fecha, monto, codPago, codReserva)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal pago.")
    else:
        print(f"Pago actualizado.")

def eliminar_pago(db):
    conection = db.cursor()
    codReserva = input("ID de la Reserva: ")
    codPago = input("ID del pago: ")
    
    query = "DELETE FROM PAY WHERE Pay_ID=%s AND Boo_ID=%s"
    values = (codPago, codReserva)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal pago.")
    else:
        print(f"Pago eliminado.")

def menu_crud_pagos(db):
    while True:
        print(msj.opcionesPago)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_pago(db)
        elif opcion == "2":
            consultar_pagos(db)
        elif opcion == "3":
            actualizar_pago(db)
        elif opcion == "4":
            eliminar_pago(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
