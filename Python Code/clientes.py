import mensajes as msj

def insertar_cliente(db):
     cedula = input("Cédula: ")
     nombre = input("Nombre: ")
     apellido = input("Apellido: ")
     correo = input("Correo: ")
     celular = input("Celular: ")
     sexo = input("Sexo (M-F): ")
     conection = db.cursor()
     tupla = (cedula, nombre, apellido, celular, correo, sexo)
     sql = "INSERT INTO CUSTOMER (Cus_ID, Cus_FName, Cus_LName, Cus_Phone, Cus_Email, Cus_Sex) VALUES (%s, %s, %s, %s, %s, %s)" 
     conection.execute(sql,tupla)
     db.commit()
     print(f"Cliente {nombre} {apellido} agregado.")

def consultar_clientes(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM CUSTOMER")
    datos = conection.fetchall()
    for i in datos:
      print(i)

def actualizar_cliente(db):
    conection = db.cursor()
    cedula = input("Ingrese la cédula del cliente a actualizar: ")
    telefono = input("Ingrese el teléfono actualizado: ")
    email = input("Ingrese el e-mail actualizado: ")

    query = "UPDATE CUSTOMER SET Cus_Phone=%s, Cus_email=%s WHERE Cus_ID=%s"
    values = (telefono, email, cedula)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún cliente con ese ID.")
    else:
      print(f"Cliente actualizado.") 

def eliminar_cliente(db):
    conection = db.cursor()
    cedula = input("Ingrese la cédula del cliente a eliminar: ")

    query = "DELETE FROM CUSTOMER WHERE Cus_ID=%s"
    values = (cedula,)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún cliente con ese ID.")
    else:
        print(f"Cliente eliminado.")


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
