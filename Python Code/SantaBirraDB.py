from dotenv import load_dotenv
from ventas import *
from clientes import *
from productos import *
<<<<<<< HEAD
from reportes import *
from ventas import *

import mensajes as msj
=======
from inventario import *
>>>>>>> gatumbac

def menu_principal(db):
<<<<<<< HEAD
    while(True):
        print(msj.opcionesMenu)
        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
=======
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
>>>>>>> gatumbac
            menu_crud_clientes(db)
        elif opcion == 2:
            menu_crud_productos(db)
<<<<<<< HEAD
        elif opcion == 3:
            menu_crud_proveedores(db)
        elif opcion == 4:
=======
        elif opcion == "3":
            menu_crud_inventario(db)
        elif opcion == "4":
>>>>>>> gatumbac
            menu_crud_ventas(db)
        elif opcion == 5:
            menu_crud_reportes(db)
        elif opcion == 6:
            break
        else:
            print(msj.opcionesError)
