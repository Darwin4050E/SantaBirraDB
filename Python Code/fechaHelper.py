from datetime import datetime

def getFecha():
    opcion = pedirOpcionFecha()
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

def pedirOpcionFecha():
    print("\nOpciones para la fecha.\n1. Seleccionar Fecha Actual.\n2. Ingresar Fecha.")
    opciones = [1,2]
    opcion = input("Ingrese una opción: ")
    while ((not opcion.isdigit()) or (int(opcion) not in opciones)):
        print("Ingrese una opción válida")
        opcion = input("Ingrese una opción: ")
    return int(opcion)
