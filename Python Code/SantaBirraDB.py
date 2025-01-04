from dotenv import load_dotenv
import os
import mysql.connector 

# --- Menú Principal ---
def menu_principal(db):
    while True:
        print("""
        === Bienvenido al sistema Santa Birra ===
        == Seleccione una opción ==
        1. Gestión de Clientes
        2. Gestión de Productos
        3. Gestión de Reservas
        4. Gestión de Ventas
        5. Generar Reportes
        6. Salir
        """)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_crud_clientes(db)
        elif opcion == "2":
            menu_crud_productos(db)
        elif opcion == "3":
            menu_crud_reservas(db)
        elif opcion == "4":
            menu_crud_ventas(db)
        elif opcion == "5":
            menu_reportes(db)
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

def menu_crud_clientes(db):
    while True:
        print("""
        === Gestión de Clientes - Santa Birra ===
        1. Insertar Cliente
        2. Consultar Clientes
        3. Actualizar Cliente
        4. Eliminar Cliente
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
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

        elif opcion == "2":
            conection = db.cursor()
            conection.execute("SELECT * FROM CUSTOMER")
            datos = conection.fetchall()
            for i in datos:
                print(i)

        elif opcion == "3":
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
            
        elif opcion == "4":
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

        elif opcion == "5":
            break

        else:
            print("Opción no válida.")

def menu_crud_productos(db):
    while True:
        print("""
        === Gestión de Productos - Santa Birra===
        1. Insertar Producto
        2. Consultar Productos
        3. Actualizar Producto
        4. Eliminar Producto
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del producto: ")
            precio = input("Precio: ")
            cat_id = input("Id de la categoría (1-10): ")
            conection = db.cursor()
            tupla = (nombre, precio, cat_id)
            sql = "INSERT INTO PRODUCT (Pro_Name, Pro_Price, Cat_ID) VALUES (%s, %s, %s) "
            conection.execute(sql,tupla)
            db.commit()
            print("Producto agregado con éxito.")

        elif opcion == "2":
            conection = db.cursor()
            conection.execute("SELECT * FROM PRODUCT")
            datos = conection.fetchall()
            for i in datos:
                print(i)

        elif opcion == "3":
            conection = db.cursor()
            producto = input("Ingrese el nombre del producto a actualizar: ")
            precio = input("Ingrese el precio actualizado: ")

            query = "UPDATE PRODUCT SET Pro_Price=%s WHERE Pro_Name=%s"
            values = (precio, producto)
            
            conection.execute(query, values)
            db.commit()
            if conection.rowcount == 0:
                print("No se encontró ningún producto con ese nombre.")
            else:
                print(f"Producto actualizado.")

        elif opcion == "4":
            conection = db.cursor()
            producto = input("Ingrese el nombre del producto a eliminar: ")

            query = "DELETE FROM PRODUCT WHERE Pro_Name=%s"
            values = (producto, )
            
            conection.execute(query, values)
            db.commit()
            if conection.rowcount == 0:
                print("No se encontró ningún producto con ese nombre.")
            else:
                print(f"Producto eliminado.")

        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

# Programa
load_dotenv()

MYSQLSERVER = os.getenv("MYSQL_HOST")
MYSQLDB = os.getenv("MYSQL_DB")
MYSQLUSER = os.getenv("MYSQL_USER")
MYSQLPASS = os.getenv("MYSQL_PASS")


db = mysql.connector.connect(
    host = MYSQLSERVER,
    user = MYSQLUSER,
    password = MYSQLPASS,
    database = "SANTABIRRADB"
)

# Iniciar el programa
menu_principal(db)
