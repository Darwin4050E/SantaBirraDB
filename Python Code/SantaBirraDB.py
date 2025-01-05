from dotenv import load_dotenv
import os
import mysql.connector
from ventas import *
from clientes import *
from productos import *
from inventario import *

# --- Menú Principal ---
def menu_principal(db):
    while True:
        print("""
        === Bienvenido al sistema Santa Birra ===
        == Seleccione una opción ==
        1. Gestión de Clientes
        2. Gestión de Productos
        3. Gestión de Inventarios
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
            menu_crud_inventario(db)
        elif opcion == "4":
            menu_crud_ventas(db)
        elif opcion == "5":
            menu_reportes(db)
        elif opcion == "6":
            print("Saliendo del sistema...")
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
