import mensajes as msj

def insertar_mienbro(db):
     cedula = input("Ingresa la cédula del empleado: ")
     nombre = input("Ingresa el nombre del empleado: ")
     apellido = input("Ingresa el apellido del empleado: ")
     experiencia = int(input("Ingresa la experiencia del empleado: "))
     rol = input("Ingresa el rol \nG- si es guarida\nP si es promotor\nS si es vendedor\nM si es manager:")
     while rol not in ["G", "P", "S", "M"]:
         rol = input("Ingresa el rol \nG- si es guarida\nP si es promotor\nS si es vendedor\nM si es manager:")
     conection = db.cursor()
     tupla = (cedula, nombre, apellido, experiencia, rol)
     sql = "INSERT INTO MEMBER (Mem_ID, Mem_FName, Mem_LName, Mem_experience, Mem_rol) VALUES (%s, %s, %s, %s, %s)" 
     conection.execute(sql,tupla)
     db.commit()
     if rol == "G":
         sql1 = "INSERT INTO GUARD (Mem_ID) VALUES (%s)"
         tupla1 = (cedula,)
         conection.execute(sql1,tupla1)
         db.commit()
     elif rol == "P":
         comision = input("Ingresa la comisión: ")
         manger = input("Ingresa el ID del manager: ")
         sql1 = "INSERT INTO PROMOTOR (Mem_ID, Prom_com, Mem_MAn) VALUES (%s,%s,%s)"
         tupla1 = (cedula, comision, manger)
         conection.execute(sql1,tupla1)
         db.commit()
     elif rol == "S":
         sql1 = "INSERT INTO SELLER (Mem_ID) VALUES (%s)"
         tupla1 = (cedula,)
         conection.execute(sql1,tupla1)
         db.commit()
     else:
         sql1 = "INSERT INTO MANAGER (Mem_ID) VALUES (%s)"
         tupla1 = (cedula,)
         conection.execute(sql1,tupla1)
         db.commit()

  
                 
     print(f"Empleado {nombre} {apellido} agregado.")

def consultar_empleados(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM MEMBER")
    datos = conection.fetchall()
    for i in datos:
      print(i)

def actualizar_empleado(db):
    conection = db.cursor()
    cedula = input("Ingrese la cédula del empleado a actualizar: ")
    experiencia = input("Ingrese la experiencia actualizada: ")

    query = "UPDATE MEMBER SET Mem_experience=%s WHERE Mem_ID=%s"
    values = (experiencia, cedula)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún empleado con ese ID.")
    else:
      print(f"empleado actualizado.") 

def eliminar_empleado(db):
    conection = db.cursor()
    cedula = input("Ingrese la cédula del empleado a eliminar: ")

    query = "DELETE FROM MEMBER WHERE Mem_ID=%s"
    values = (cedula,)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró empleado con ese ID.")
    else:
        print(f"Empleado eliminado.")


def menu_crud_empleados(db):
    while True:
        print(msj.opcionesEmpleado)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            insertar_mienbro(db)
        elif opcion == "2":
            consultar_empleados(db)
        elif opcion == "3":
            actualizar_empleado(db)   
        elif opcion == "4":
            eliminar_empleado(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
