def pedirEnteroPositivo(mensaje):
    numero = input(mensaje)
    while(not numero.isdigit() or int(numero) < 0):
        print("Ingrese una entrada válida.")
        numero = input(mensaje)
    return int(numero)