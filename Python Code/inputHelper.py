def pedirEnteroPositivo(mensaje):
    numero = input(mensaje)
    while(not numero.isdigit() or int(numero) < 0):
        print("Ingrese una entrada válida.")
        numero = input(mensaje)
    return int(numero)

def pedirNatural(mensaje):
    numero = input(mensaje)
    while(not numero.isdigit() or int(numero) <= 0):
        print("Ingrese una entrada válida.")
        numero = input(mensaje)
    return int(numero)

def pedirDecimalPositivo(mensaje):
    numero = input(mensaje)
    while(not numero.replace(".","").isdigit() or float(numero) < 0):
        print("Ingrese una entrada válida.")
        numero = input(mensaje)
    return float(numero)

def pedirPorcentaje(mensaje):
    numero = input(mensaje)
    while(not (numero.replace(".","").isdigit() and 0 <= float(numero) <= 1)):
        print("Ingrese un porcentaje válido.")
        numero = input(mensaje)
    return float(numero)

def pedirCedula(mensaje):
    cedula = input(mensaje)
    while(not cedula.isdigit() or len(cedula) != 10):
        print("Ingrese una identificación válida.")
        cedula = input(mensaje)
    return cedula

def pedirTelefono(mensaje):
    telefono = input(mensaje)
    while(not telefono.isdigit() or len(telefono) != 10):
        print("Ingrese un teléfono válido.")
        telefono = input(mensaje)
    return telefono

def pedirTelefonoConvencional(mensaje):
    telefono = input(mensaje)
    longitudes = [9,10]
    while(not telefono.isdigit() or len(telefono) not in longitudes):
        print("Ingrese un teléfono válido.")
        telefono = input(mensaje)
    return telefono

def pedirNombre(mensaje):
    nombre = input(mensaje)
    while(not nombre.isalpha() or len(nombre) < 2):
        print("Ingrese un nombre válido.")
        nombre = input(mensaje)
    return nombre

def pedirApellido(mensaje):
    nombre = input(mensaje)
    while(not nombre.isalpha() or len(nombre) < 2):
        print("Ingrese un apellido válido.")
        nombre = input(mensaje)
    return nombre

def pedirNombreEmpresa(mensaje):
    nombre = input(mensaje)
    while(len(nombre) < 2):
        print("Ingrese un nombre válido.")
        nombre = input(mensaje)
    return nombre

def pedirNombreConSignos(mensaje):
    nombre = input(mensaje)
    while(len(nombre) < 2):
        print("Ingrese un nombre válido.")
        nombre = input(mensaje)
    return nombre

def pedirCorreo(mensaje):
    correo = input(mensaje)
    while not ("@" in correo and "." in correo.split("@")[-1]):
        print("Ingrese un correo válido.")
        correo = input(mensaje)
    return correo

def pedirSexo(mensaje):
    sexo = input(mensaje)
    while sexo not in ["M","F"]:
        print("Ingrese un sexo válido.")
        sexo = input(mensaje)
    return sexo

def pedirRUC(mensaje):
    ruc = input(mensaje)
    while(not ruc.isdigit() or len(ruc) != 13):
        print("Ingrese un RUC válido.")
        ruc = input(mensaje)
    return ruc

def pedirEntreDosOpciones(mensajeOpciones, opcionUno, opcionDos):
    print(f"\n{mensajeOpciones}.\n1. {opcionUno}.\n2. {opcionDos}.")
    opciones = [1,2]
    opcion = input("Ingrese una opción: ")
    while ((not opcion.isdigit()) or (int(opcion) not in opciones)):
        print("Ingrese una opción válida.")
        opcion = input("Ingrese una opción: ")
    return int(opcion)

def pedirSiONo(mensaje):
    inputUsuario = input(mensaje).lower()
    opciones = ["s","n"]
    while inputUsuario not in opciones:
        print("Ingrese una opción válida.")
        inputUsuario = input(mensaje).lower()
    return inputUsuario 

def pedirDescripcion(mensaje):
    descripcion = input(mensaje)
    while len(descripcion) < 5:
        print("Ingrese una descripción válida.")
        descripcion = input(mensaje)
    return descripcion

def pedirUnidadMedidad(mensaje):
    descripcion = input(mensaje)
    while not (descripcion[:-2].isdigit() and descripcion[-2:].isalpha() and len(descripcion) > 2):
        print("Ingrese una unidad válida junto con su valor numérico (ejemplo: 15ml).")
        descripcion = input(mensaje)
    return descripcion

def pedirIdEntero(mensaje):
    id = input(mensaje)
    while not id.isdigit() or int(id) <= 0:
        print("Ingrese un ID válido.")
        id = input(mensaje)
    return int(id)
