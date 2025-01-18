import mensajes as msj
from prettytable import PrettyTable

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

def reporteGastosProveedor(db):
    query = 'SELECT Sup_RUC, Sup_Name, Sup_Total FROM V_COMPRAS_GASTOSPROVEEDOR'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        tabla = PrettyTable()
        tabla.field_names = ["RUC", "Proveedor", "Gasto"]
        print("")
        for dato in datos:
            ruc = dato[0]
            Proveedor = dato[1]
            Gasto = dato[2]
            tabla.add_row([ruc, Proveedor, Gasto])
        print(tabla)
    
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
            print(f"Inventario: {dato[0]} - Código de producto: {dato[1]} - Producto: {dato[2]} - Cantidad: {dato[3]}")
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
        opcion = int(input("Selecciona una opción [1-5]: "))
        if(opcion == 1):
            reporteVentas(db)
        elif(opcion == 2):
            reporteInventario(db)
        elif(opcion == 3):
            reporteRendimientoEventos(db)
        elif(opcion == 4):
            reporteGastosProveedor(db)
        elif(opcion == 5):
            return
        else:
            print(msj.opcionesError)