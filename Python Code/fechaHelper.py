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

def getHora():
    opcion = pedirEntreDosOpciones("Opciones para la hora", "Seleccionar Hora Actual", "Ingresar Hora")
    if opcion == 1:
        return getHoraActual()
    elif opcion == 2:
        return getHoraUsuario()

def getHoraActual():
    return datetime.today().time()

def getHoraUsuario():
    while True:
        horaIngresada = input("Hora (HH:MM): ")
        try:
            hora = datetime.strptime(horaIngresada, "%H:%M").time()
            return hora
        except ValueError:
            print("Hora inválida. Por favor, ingrese una hora en el formato HH:MM.")
