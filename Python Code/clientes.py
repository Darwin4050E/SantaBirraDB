import mensajes as msj
from validadorFK import *
from inputHelper import *
from outputHelper import *

def insertar_cliente(db):
    cedula = pedirCedula("Cédula: ")
    nombre = pedirNombre("Nombre: ")
    apellido = pedirApellido("Apellido: ")
    correo = pedirCorreo("Correo: ")
    celular = pedirTelefono("Celular: ")
    sexo = pedirSexo("Sexo (M/F): ")

    conection = db.cursor()
    tupla = (cedula, nombre, apellido, celular, correo, sexo)
    sql = "INSERT INTO CUSTOMER (Cus_ID, Cus_FName, Cus_LName, Cus_Phone, Cus_Email, Cus_Sex) VALUES (%s, %s, %s, %s, %s, %s)" 
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def consultar_clientes(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM CUSTOMER")
    datos = conection.fetchall()
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        apellido = fila[2]
        celular = fila[3]
        correo = fila[4]
        sexo = fila[5]
        print(f"id: {cedula} - nombre: {nombre} - apellido: {apellido} - correo: {correo} - celular: {celular} - sexo: {sexo}")

def actualizar_cliente(db):
    conection = db.cursor()
    cedula = pedirCedula("Cédula: ")
    if not validar_clave_foranea(db, "CUSTOMER", "Cus_ID", cedula):
        printMensajeErrorFK()
        return

    celular = pedirTelefono("Celular actualizado: ")
    correo = pedirCorreo("Correo actualizado: ")

    query = "UPDATE CUSTOMER SET Cus_Phone=%s, Cus_email=%s WHERE Cus_ID=%s"
    values = (celular, correo, cedula)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_cliente(db):
    conection = db.cursor()
    cedula = pedirCedula("Cédula: ")

    query = "DELETE FROM CUSTOMER WHERE Cus_ID=%s"
    values = (cedula,)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        printMensajeErrorFK()
    else:
        printEliminacionExitosa()

def menu_crud_clientes(db):
    while True:
        print(msj.opcionesCliente)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            insertar_cliente(db)
        elif opcion == "2":
            consultar_clientes(db)
        elif opcion == "3":
            consultar_clientes(db)
            actualizar_cliente(db)   
        elif opcion == "4":
            consultar_clientes(db)
            eliminar_cliente(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)