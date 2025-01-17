from validadorFK import *
from datetime import *
import mensajes as msj
from inputHelper import *
from outputHelper import *
from fechaHelper import *
from prettytable import PrettyTable

def insert_pago(db):
    conection = db.cursor()
    codReserva = pedirIdEntero("ID de la Reserva: ")

    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", codReserva):
        printMensajeErrorFK()
        return
    
    codPago = ultimo_IDpago(db, codReserva) + 1
    fecha = getFecha()
    monto = pedirDecimalPositivo("Ingrese el monto del pago: ")

    tupla = (codPago, codReserva,  fecha, monto)
    sql = "INSERT INTO PAY (Pay_ID, Boo_ID, Pay_Date, Pay_Amount) VALUES (%s, %s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def existe_pago(db, codReserva):
    conection = db.cursor()
    query = f"SELECT COUNT(*) FROM PAY WHERE Boo_ID = %s"
    conection.execute(query, (codReserva, ))
    return conection.fetchone()[0] > 0

#Saca el último ID artificial de la secuencia de inventarios del producto
def ultimo_IDpago(db, idReserva):
    conection = db.cursor()
    if existe_pago(db, idReserva):
        query = "SELECT Pay_ID FROM PAY WHERE Boo_ID = %s ORDER BY Pay_ID DESC LIMIT 1"
        conection.execute(query, (idReserva, ))
        ic_id = conection.fetchone()
        return int(ic_id[0])
    else:
        return 0

def validar_IDpago(db, idReserva, idPago):
    conection = db.cursor()
    query = "SELECT COUNT(*) FROM PAY WHERE Boo_ID = %s AND Pay_ID = %s"
    conection.execute(query, (idReserva, idPago))
    return conection.fetchone()[0] > 0

def consultar_pagos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PAY ORDER BY Boo_ID, Pay_ID ASC")
    datos = conection.fetchall()
    tabla = PrettyTable()
    tabla.field_names = ["ID Pago", "ID Reserva", "Fecha", "Monto"]
    for fila in datos:
        id = fila[0]
        reservaId = fila[1]
        fecha = fila[2].strftime("%d/%m/%Y")
        monto = fila[3]
        tabla.add_row([id, reservaId, fecha, monto])
    print(tabla)
    
def actualizar_pago(db):
    consultar_pagos(db)
    conection = db.cursor()
    codReserva = pedirIdEntero("ID de la Reserva: ")
    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", codReserva):
        printMensajeErrorFK()
        return

    codPago = pedirIdEntero("ID del pago de tal reserva: ")
    if not validar_IDpago(db, codReserva, codPago):
        print("No se encontró tal pago.")
        return

    fecha = getFecha()

    monto = pedirDecimalPositivo("Ingrese el monto actualizado del pago: ")

    query = "UPDATE PAY SET Pay_Date=%s, Pay_Amount=%s WHERE Pay_ID = %s AND Boo_ID=%s"
    values = (fecha, monto, codPago, codReserva)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_pago(db):
    consultar_pagos(db)
    conection = db.cursor()
    codReserva = pedirIdEntero("ID de la Reserva: ")
    if not validar_clave_foranea(db, "BOOKING", "Boo_ID", codReserva):
        printMensajeErrorFK()
        return

    codPago = pedirIdEntero("ID del pago de tal reserva: ")
    if not validar_IDpago(db, codReserva, codPago):
        print("No se encontró tal pago.")
        return
    
    query = "DELETE FROM PAY WHERE Pay_ID=%s AND Boo_ID=%s"
    values = (codPago, codReserva)
            
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

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
