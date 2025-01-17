import mensajes as msj
from validadorFK import *
from inputHelper import *
from outputHelper import *
from prettytable import PrettyTable
import mysql.connector as mysql


def insertar_cliente(db):
    cedula = pedirCedula("Cédula: ")
    if validar_clave_foranea(db, "CUSTOMER", "Cus_ID", cedula):
        printMensajeIngresoExistente()
        return
    
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
    tabla = PrettyTable()
    tabla.field_names = ["Cédula", "Nombre", "Apellido", "Celular", "Correo", "Sexo"]
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        apellido = fila[2]
        celular = fila[3]
        correo = fila[4]
        sexo = fila[5]
        tabla.add_row([cedula, nombre, apellido, celular, correo, sexo])
    print(tabla)

def consultar_clientesBasico(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM CUSTOMER")
    datos = conection.fetchall()
    tabla = PrettyTable()
    tabla.field_names = ["Cédula", "Nombre", "Apellido"]
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        apellido = fila[2]
        tabla.add_row([cedula, nombre, apellido])
    print(tabla)

def actualizar_cliente(db):
    consultar_clientes(db)
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
    consultar_clientesBasico(db)
    cedula = pedirCedula("Cédula: ")

    try: 
        conection = db.cursor()
        query = "DELETE FROM CUSTOMER WHERE Cus_ID=%s"
        values = (cedula,)
                
        conection.execute(query, values)
        db.commit()
        if conection.rowcount == 0:
            printMensajeErrorFK()
        else:
            printEliminacionExitosa()
    except mysql.Error as e:
        db.rollback()
        print("No se pudo eliminar el cliente porque hay ventas o reservas asociadas a él.")
    

def menu_crud_clientes(db):
    while True:
        print(msj.opcionesCliente)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            insertar_cliente(db)
        elif opcion == "2":
            consultar_clientes(db)
        elif opcion == "3":
            actualizar_cliente(db)   
        elif opcion == "4":
            eliminar_cliente(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)