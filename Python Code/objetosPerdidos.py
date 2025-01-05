from validadorFK import *
from datetime import *
import mensajes as msj

def insert_object(db):
    conection = db.cursor()
    codZona = input("ID de la Zona: ")

    if not validar_clave_foranea(db, "ZONE", "Zon_ID", codZona):
        print("No existe Zona con ese ID")
        return
    
    descripcion = input("Descripción del objeto: ")
    fechaIngresada = input("Fecha del incidente (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()

    tupla = (fecha, descripcion, codZona)
    sql = "INSERT INTO LOSTOBJECT (Los_Date, Los_Des, Zon_ID) VALUES (%s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    print("Objeto perdido agregado con éxito.")

def consultar_objetos(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM LOSTOBJECT")
    datos = conection.fetchall()
    for fila in datos:
        id = fila[0]
        fecha = fila[1].strftime("%d/%m/%Y")
        descripcion = fila[2]
        zona = fila[3]
        print(f"id: {id} - fecha: {fecha} - descripcion: {descripcion} - zonaId: {zona}")

def actualizar_objeto(db):
    conection = db.cursor()
    codObjeto = input("ID del objeto perdido: ")

    fechaIngresada = input("Fecha del objeto perdido actualizada (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()
    descripcion = input("Descripción del objeto: ")

    query = "UPDATE LOSTOBJECT SET Los_Date=%s, Los_Des=%s WHERE Los_ID=%s"
    values = (fecha, descripcion, codObjeto)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal objeto.")
    else:
        print(f"Objeto actualizado.")


def eliminar_objeto(db):
    conection = db.cursor()
    codObjeto = input("ID del objeto perdido: ")

    query = "DELETE FROM LOSTOBJECT WHERE Los_ID=%s"
    values = (codObjeto, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró tal objeto.")
    else:
        print(f"Objeto eliminado.")

def menu_crud_objetosperdidos(db):
    while True:
        print(msj.opcionesObjetoPerdido)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insert_object(db)

        elif opcion == "2":
            consultar_objetos(db)

        elif opcion == "3":
            actualizar_objeto(db)

        elif opcion == "4":
            eliminar_objeto(db)

        elif opcion == "5":
            break

        else:
            print(msj.opcionesError)
