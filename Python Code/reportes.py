import mensajes as msj

def reporteVentas(db):
    query = 'SELECT SUM(ProSale_Quantity * Pro_Price) FROM Product_Sale NATURAL JOIN Product'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        totalVentas = cursor.fetchall()
        print(msj.reporteVentas)
        print(f"Valor total en ventas de productos: ${totalVentas[0][0]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def reporteCompras(db):
    query = 'SELECTO * FROM VW_COMPRAS_GASTOSPROVEEDOR'
    try:
        cursor = db.cursor(query)
        datos = cursor.fetchall()
        for dato in datos:
            print(f"Proveedor: {dato[0]} - Gasto: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def reporteInventario(db):
    query = 'SELECT Inv_ID, Pro_Code, Pro_Name, Pro_Price FROM Inventory NATURAL JOIN Product'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print(msj.reporteInventarios)
        for dato in datos:
            print(f"Inventario: {dato[0]} - Código de producto: {dato[1]} - Producto: {dato[2]} - Cantidad: {3}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        
def reporteRendimientoEventos(db):
    query = 'SELECT Eve_Name, COUNT(Boo_ID) as count_boo FROM Booking NATURAL JOIN Event GROUP BY Eve_Name ORDER BY count_boo DESC'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        print(msj.rendimientoEventos)
        for dato in datos:
            print(f"Evento: {dato[0]} - Reserva: {dato[1]}")
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def menu_crud_reportes(db):
    while(True):
        print(msj.opcionesReporte)
        opcion = int(input("Selecciona una opción [1-4]: "))
        if(opcion == 1):
            reporteVentas(db)
        elif(opcion == 2):
            reporteInventario(db)
        elif(opcion == 3):
            reporteRendimientoEventos(db)
        elif(opcion == 4):
            reporteCompras(db)
        elif(opcion == 5):
            return
        else:
            print(msj.opcionesError)