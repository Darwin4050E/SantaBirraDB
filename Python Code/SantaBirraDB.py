from dotenv import load_dotenv
from ventas import *
from clientes import *
from productos import *
from reportes import *
from ventas import *
from proveedores import *


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
            menu_crud_compras(db)
        elif opcion == 5:
            menu_crud_empleados(db)
        elif opcion == 6:
            menu_crud_ventas(db)
        elif opcion == 7:
            menu_crud_inventario(db)
        elif opcion == 8:
            menu_crud_reservas(db)
        elif opcion == 9:
            menu_crud_promociones(db)
        elif opcion == 10:
            menu_crud_pagos(db)
        elif opcion == 11:
            menu_crud_zonas(db)
        elif opcion == 12:
            menu_crud_incidentes(db)
        elif opcion == 13:
            menu_crud_objetosperdidos(db)
        elif opcion == 14:
            menu_crud_reportes(db)
        elif opcion == 15:
            break
        else:
            print(msj.opcionesError)
