from datetime import datetime
from inputHelper import *

def getFecha():
    opcion = pedirEntreDosOpciones("Opciones para la fecha", "Seleccionar Fecha Actual", "Ingresar Fecha")
    if opcion == 1:
        return getFechaActual()
    elif opcion == 2:
        return getFechaUsuario()

def getFechaActual():
    return datetime.today().date() 

def getFechaUsuario():
    while True:
        fechaIngresada = input("Fecha (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()
            return fecha
        except ValueError:
            print("Fecha inválida. Por favor, ingrese una fecha en el formato YYYY-MM-DD.")
