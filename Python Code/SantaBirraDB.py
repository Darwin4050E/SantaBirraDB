from dotenv import load_dotenv
from ventas import *
from clientes import *
from productos import *
from reportes import *
from ventas import *

import mensajes as msj

def menu_principal(db):
    while(True):
        print(msj.opcionesMenu)
        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
            menu_crud_clientes(db)
        elif opcion == 2:
            menu_crud_productos(db)
        elif opcion == 3:
            menu_crud_proveedores(db)
        elif opcion == 4:
            menu_crud_ventas(db)
        elif opcion == 5:
            menu_crud_reportes(db)
        elif opcion == 6:
            break
        else:
            print(msj.opcionesError)
