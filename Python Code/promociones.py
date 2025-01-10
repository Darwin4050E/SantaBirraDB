import mensajes as msj
from inputHelper import *
from outputHelper import *
from validadorFK import *

def insert_promociones(db):
    nombrePromocion = pedirNombreConSignos("Nombre de la promoción: ")
    descuento = pedirPorcentaje("Descuento asociado a la promoción (0.xx): ")

    conection = db.cursor()
    tupla = (nombrePromocion, descuento)
    sql = "INSERT INTO PROMOTION (Prom_Name, Prom_Descuento) VALUES (%s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    printIngresoExitoso()

def consultar_promociones(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM PROMOTION")
    datos = conection.fetchall()
    for fila in datos:
        id = fila[0]
        nombre = fila[1]
        descuento = fila[2]
        print(f"id: {id} - nombre: {nombre} - descuento: {descuento}")

def actualizar_promocion(db):
    consultar_promociones(db)
    conection = db.cursor()
    codProm = pedirEnteroPositivo("Ingrese el ID de la promoción: ")
    if not validar_clave_foranea(db, "PROMOTION", "Prom_ID", codProm):
        printMensajeErrorFK()
        return
    
    nombrePromocion = pedirNombreConSignos("Nombre de la promoción actualizado: ")
    descuento = pedirPorcentaje("Descuento asociado a la promoción actualizado (0.xx): ")

    query = "UPDATE PROMOTION SET Prom_Name=%s, Prom_Descuento=%s WHERE Prom_ID = %s"
    values = (nombrePromocion, descuento, codProm)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_promocion(db):
    consultar_promociones(db)
    conection = db.cursor()
    codProm = pedirEnteroPositivo("Ingrese el ID de la promoción: ")
    if not validar_clave_foranea(db, "PROMOTION", "Prom_ID", codProm):
        printMensajeErrorFK()
        return

    query = "DELETE FROM PROMOTION WHERE Prom_ID=%s"
    values = (codProm, )
            
    conection.execute(query, values)
    db.commit()
    printEliminacionExitosa()

def menu_crud_promociones(db):
    while True:
        print(msj.opcionesPromocion)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            insert_promociones(db)
        elif opcion == "2":
            consultar_promociones(db)
        elif opcion == "3":
            actualizar_promocion(db)
        elif opcion == "4":
            eliminar_promocion(db)
        elif opcion == "5":
            break
        else:
            print(msj.opcionesError)
