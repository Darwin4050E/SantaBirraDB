import mensajes as msj

def consultar_zonas(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM ZONE")
    datos = conection.fetchall()
    for fila in datos:
        id_zona = fila[0]
        capacidad = int(fila[1])
        tipo = fila[2]
        codGuardia = fila[3]
        if tipo == 'G':
            tipo = 'General'
        else:
            tipo = 'VIP'
        print(f"id: {id_zona} - capacidad: {capacidad} - tipo: {tipo} - guardia: {codGuardia}")

def actualizar_zonaVIP(db):
    conection = db.cursor()
    capacidad = input("Ingrese la nueva capacidad: ")
    query = "UPDATE ZONE SET Zon_Capacity=%s WHERE Zon_ID=1"
    values = (capacidad,)
    conection.execute(query, values)
    db.commit()
    recargo = input("Ingrese el nuevo recargo: ")
    query = "UPDATE ZoneVIP SET Charge_VIP=%s WHERE Zon_ID=1"
    values = (recargo, )
    conection.execute(query, values)
    db.commit()
    print(f"Zona actualizada con éxito.")

def actualizar_zonaGeneral(db): 
    conection = db.cursor()
    capacidad = input("Ingrese la nueva capacidad: ")
    query = "UPDATE ZONE SET Zon_Capacity=%s WHERE Zon_ID=2"
    values = (capacidad, )
    conection.execute(query, values)
    db.commit()
    print(f"Zona actualizada con éxito.")

def actualizar_zona(db):
    conection = db.cursor()
    codZona = int(input("Ingrese el código de la zona a actualizar: "))
    if codZona == 1:
        actualizar_zonaVIP(db)
    elif codZona == 2:
        actualizar_zonaGeneral(db)
    else: 
        print("No se encontró la zona con ese ID.")

def menu_crud_zonas(db):
    while True:
        print(msj.opcionesZona)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            print("No es posible agregar más zonas a la discoteca.")
        elif opcion == "2":
            consultar_zonas(db)
        elif opcion == "3":
            actualizar_zona(db)
        elif opcion == "4":
            print("No es posible eliminar zonas de la discoteca.")
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)