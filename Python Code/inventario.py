from datetime import datetime
def insert_inventario(db):
    codigoProd = input("Código del producto: ")
    stock = input("Stock del producto: ")
    fechaIngresada = input("Fecha del inventario (YYYY-MM-DD): ")
    fecha = datetime.strptime(fechaIngresada, "%Y-%m-%d").date()
    conection = db.cursor()
    tupla = (fecha, stock, codigoProd)
    sql = "INSERT INTO INVENTORY (Inv_Date, Inv_Stock, Pro_Code) VALUES (%s, %s, %s) "
    conection.execute(sql,tupla)
    db.commit()
    print("Inventario agregado con éxito.")


def consultar_inventario(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM INVENTORY")
    datos = conection.fetchall()
    for fila in datos:
        id_inventario = fila[0]
        fecha = fila[1].strftime("%d/%m/%Y")
        stock = int(fila[2]) 
        codigoProd = fila[3]

        print(f"id: {id_inventario} - fecha: {fecha} - stock: {stock} - codigo: {codigoProd}")

def obtener_ultimo_inventario(db, codProd):
    conection = db.cursor()
    query = "SELECT Inv_ID FROM INVENTORY WHERE Pro_Code=%s ORDER BY Inv_Date DESC LIMIT 1"
    tupla = (codProd, )
    conection.execute(query, tupla)
    inventario = conection.fetchone()
    if inventario is not None:
        return inventario[0]  # Retorna el ID del inventario
    else:
        return None  # Si no se encontró, retorna None


def actualizar_inventario(db):
    conection = db.cursor()
    codProd = input("Ingrese el código del producto a actualizar: ")
    inventario = obtener_ultimo_inventario(db, codProd)
    if inventario is None:
        print("No se encontró el producto.")
        return
    
    stock = input("Ingrese el stock a actualizar: ")

    fechaActual = datetime.today().date() 

    query = "UPDATE INVENTORY SET Inv_Stock=%s, Inv_Date=%s WHERE Inv_ID = %s"
    values = (stock, fechaActual, inventario)
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con ese ID.")
    else:
        print(f"Inventario actualizado.")


def eliminar_inventario(db):
    conection = db.cursor()
    #Se eliminará el último inventario
    codProd = input("Ingrese el código del producto para eliminar el ultimo inventario: ")
    inventario = obtener_ultimo_inventario(db, codProd)
    if inventario is None:
        print("No se encontró el producto.")
        return

    query = "DELETE FROM INVENTORY WHERE Inv_ID=%s"
    values = (inventario, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        print("No se encontró ningún producto con ese ID")
    else:
        print(f"Inventario eliminado.")

def menu_crud_inventario(db):
    while True:
        print("""
        === Gestión de Inventario - Santa Birra===
        1. Insertar Inventario
        2. Consultar Inventario
        3. Actualizar Inventario
        4. Eliminar Inventario
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insert_inventario(db)

        elif opcion == "2":
            consultar_inventario(db)

        elif opcion == "3":
            actualizar_inventario(db)

        elif opcion == "4":
            eliminar_inventario(db)

        elif opcion == "5":
            break

        else:
            print("Opción no válida.")
