
# Ejercicio 11:
def actualizarInventario(diccionario):
    listaVentas = []
    opcion = 1
    while(opcion != 0):
        producto = input("Ingrese el nombre del producto: ")
        ventas = int(input("Ingrese la cantidad de productos vendidos: "))
        listaVentas.append([producto, ventas])
        opcion = int(input("\nPulse cualquier número para seguir actualizando o 0 para dejar de hacerlo.\n"))
    for elemento in listaVentas:
        producto = elemento[0]
        ventas = elemento[1]
        if producto in diccionario:
            diccionario[producto] -= ventas
            if diccionario[producto] <= 0:
                del diccionario[producto]
    print(f"El inventario actual es {diccionario}")

# Ejercicio 12:
def calcularPromedio(diccionario, estudiante):
    promedio = 0
    if estudiante in diccionario:
        materias = diccionario[estudiante]
        for valor in materias.values():
            promedio += valor
    else:
        print("El estudiante ingresado no existe.")
    return promedio

def imprimirPromediosSuperioresA(diccionario, mínimo):
    for estudiante in diccionario:
        promedio = calcularPromedio(diccionario, estudiante)
        if promedio >= 8:
            print(f"El estudiante {estudiante} tiene un promedio de {promedio}")

# Ejercicio 13:
def analizarTexto(texto):
    diccionarioPalabras = []
    listaCadena = texto.lower().split(" ")
    for elemento in listaCadena:
        longitudCadena = len(elemento)
        if longitudCadena >= 3:
            diccionarioPalabras[elemento] = texto.count(elemento)
    return diccionarioPalabras

# Ejercicio 14:
def unirDiccionarios(diccionario1, diccionario2):
    diccionarioResultante = diccionario1.copy()
    for clave in diccionario2.keys():
        if clave in diccionario1:
            diccionarioResultante[clave] += diccionario2[clave]
        else:
            diccionarioResultante[clave] = diccionario2[clave]
    return diccionarioResultante

# Ejercicio 15:
def agregarProducto(diccionario):
    id = int(input("Ingrese el ID del producto: "))
    nombre = input("Ingrese el nombre del producto: ")
    cantidad = int(input("Ingrese el stock del producto: "))
    precio_unitario = float(input("Ingrese el precio unitario del producto: "))
    categoria = input("Ingrese la categoría del producto: ")
    diccionario[id] = {"nombre":nombre, "cantidad":cantidad, "precio_unitario":precio_unitario, "categoria":categoria}
    return diccionario

def buscarProducto(diccionario, categoria):
    for item in diccionario.items():
        valor = item[1]
        if categoria == valor["categoria"]:
            print(f"ID: {item[0]}, Producto: {valor["producto"]}, Cantidad: {valor["cantidad"]}, Precio unitario: {valor["precio_unitario"]}")

def calcularInventario(diccionario):
    total = 0
    for valor in diccionario.values():
        total += valor["cantidad"] * valor["precio_unitario"]
    return total

def venderProducto(diccionario, producto, ventas):
    for valor in diccionario.values():
        if producto == valor["nombre"]:
            valor["nombre"] -= ventas
    return diccionario
