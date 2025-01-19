import mensajes as msj
from prettytable import PrettyTable

def reporteVentas(db):
    query = 'SELECT * FROM VW_REPORTE_VENTAS_PRODUCTOS'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        tabla = PrettyTable()
        tabla.field_names = ["Cod", "Nombre", "Medida", "Categoria", "Cant. Vendida", "Monto Vendido", "Ganancias"]
        for dato in datos:
            codigo = dato[0]
            producto = dato[1]
            medida = dato[2]
            categoria = dato[3]
            vendidos = dato[4]
            monto = dato[5]
            ganancias = dato[6]
            tabla.add_row([codigo, producto, medida, categoria, vendidos, monto, ganancias])
        tabla.align["Monto Vendido"] = "r"  
        tabla.align["Ganancias"] = "r" 
        print(tabla)
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
    query = 'SELECT * FROM VW_REPORTE_MINIMAS_EXISTENCIAS'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        tabla = PrettyTable()
        tabla.field_names = ["Cod", "Nombre", "Medida", "Categoria", "Stock", "F. Actualizacion", "RUC Prov.", "Proveedor"]
        for dato in datos:
            codigo = dato[0]
            producto = dato[1]
            medida = dato[2]
            categoria = dato[3]
            existencias = dato[4]
            fecha = dato[5].strftime("%d/%m/%Y")
            ruc = dato[6]
            proveedor = dato[7]
            tabla.add_row([codigo, producto, medida, categoria, existencias, fecha, ruc, proveedor])
        print(tabla)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        
def reporteReservas(db):
    query = 'SELECT * FROM VW_REPORTE_RESERVAS_COMPLETADAS'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        tabla = PrettyTable()
        tabla.field_names = ["ID", "Fecha", "Evento", "Asistentes", "Entradas $", "Descuento $", "Promotor $", "Ajuste $", "Pago $"]
        for dato in datos:
            id = dato[0]
            fecha = dato[1]
            evento = dato[3]
            asistentes = dato[4]
            entradas = dato[5]
            descuento = dato[6]
            comision = dato[7]
            total = dato[8]
            pago = dato[9]
            tabla.add_row([id, fecha, evento, asistentes, entradas, descuento, comision, total, pago])
        print(tabla)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def reporteIncidentes(db):
    query = 'SELECT * FROM VW_REPORTE_INCIDENTES_CLIENTE'
    try:
        cursor = db.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        tabla = PrettyTable()
        tabla.field_names = ["Cedula", "Nombre", "Apellido", "Incidentes", "Ultimo Incidente"]
        for dato in datos:
            cedula = dato[0]
            nombre = dato[1]
            apellido = dato[2]
            incidentes = dato[3]
            ultimo = dato[4]
            tabla.add_row([cedula, nombre, apellido, incidentes, ultimo])
        print(tabla)
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def menu_crud_reportes(db):
    while(True):
        print(msj.opcionesReporte)
        opcion = int(input("Selecciona una opción [1-6]: "))
        if(opcion == 1):
            print(msj.reporteVentas)
            reporteVentas(db)
        elif(opcion == 2):
            print(msj.reporteInventarios)
            reporteInventario(db)
        elif(opcion == 3):
            print(msj.reporteReservas)
            reporteReservas(db)
        elif(opcion == 4):
            print(msj.reporteProveedor)
            reporteGastosProveedor(db)
        elif (opcion == 5):
            print(msj.reporteIncidentes)
            reporteIncidentes(db)
        elif(opcion == 6):
            return
        else:
            print(msj.opcionesError)