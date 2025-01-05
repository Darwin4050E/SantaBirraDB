import mensajes as msj

def menu_crud_proveedores(db):
    while True:
        print(msj.opcionesProveedor)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            cedula = input("Ingrese el RUC del proveedor: ")
            nombre = input("Ingrese el nombre: ")
            celular = input("Ingrese el celular: ")
            correo = input("Ingrese el correo: ")
            conection = db.cursor()
            tupla = (cedula, nombre, celular, correo)
            sql = "INSERT INTO SUPPLIER (Sup_RUC, Sup_Name, Sup_Phone, Sup_Email) VALUES (%s, %s, %s, %s)" 
            conection.execute(sql,tupla)
            db.commit()
            print(f"Proveedor {nombre} agregado.")
        elif opcion == "2":
            conection = db.cursor()
            conection.execute("SELECT * FROM SUPPLIER")
            datos = conection.fetchall()
            for i in datos:
                print(i)
        elif opcion == "3":
            conection = db.cursor()
            cedula = input("Ingrese el RUC  del proveedor a actualizar: ")
            telefono = input("Ingrese el teléfono actualizado: ")
            email = input("Ingrese el e-mail actualizado: ")

            query = "UPDATE SUPPLIER SET Sup_Phone=%s, Sup_email=%s WHERE Sup_RUC=%s"
            values = (telefono, email, cedula)
            
            conection.execute(query, values)
            db.commit()
            if conection.rowcount == 0:
                print("No se encontró ningún cliente con ese ID.")
            else:
                print(f"Cliente actualizado.")    
        elif opcion == "4":
            conection = db.cursor()
            ruc = input("Ingrese el RUC del proveedor a eliminar: ")

            query = "DELETE FROM SUPPLIER WHERE Sup_RUC=%s"
            values = (ruc,)
            
            conection.execute(query, values)
            db.commit()
            if conection.rowcount == 0:
                print("No se encontró ningún cliente con ese ID.")
            else:
                print(f"Proveedor eliminado eliminado.")
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
