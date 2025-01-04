from prettytable import PrettyTable

# Base de datos (listas)

# --- Funciones CRUD ---
# Clientes
def insertar_cliente():
    cedula = input("Cédula: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    correo = input("Correo: ")
    celular = input("Celular: ")
    sexo = input("Sexo (M-F): ")

    print(f"Cliente {nombre, apellido} agregado.")

def consultar_clientes():
    if not clientes:
        print("No hay clientes registrados.")
        return
    
    tabla = PrettyTable()
    tabla.field_names = ["#", "Nombre", "Cédula", "Correo", "Celular"]

    for i, cliente in enumerate(clientes, start=1):
        tabla.add_row([i, cliente["nombre"], cliente["cedula"], cliente["correo"], cliente["celular"]])
    
    print(tabla)

def actualizar_cliente():
    consultar_clientes()
    index = int(input("Seleccione el cliente a actualizar: ")) - 1
    if 0 <= index < len(clientes):
        clientes[index]['nombre'] = input(f"Nuevo nombre ({clientes[index]['nombre']}): ") or clientes[index]['nombre']
        clientes[index]['cedula'] = input(f"Nueva cédula ({clientes[index]['cedula']}): ") or clientes[index]['cedula']
        clientes[index]['correo'] = input(f"Nuevo correo ({clientes[index]['correo']}): ") or clientes[index]['correo']
        clientes[index]['celular'] = input(f"Nuevo celular ({clientes[index]['celular']}): ") or clientes[index]['celular']
        print("Cliente actualizado.")
    else:
        print("Cliente no encontrado.")

def eliminar_cliente():
    consultar_clientes()
    index = int(input("Seleccione el cliente a eliminar: ")) - 1
    if 0 <= index < len(clientes):
        clientes.pop(index)
        print("Cliente eliminado.")
    else:
        print("Cliente no encontrado.")

# Productos
def insertar_producto():
    nombre = input("Nombre del producto: ")
    categoria = input("Categoría: ")
    precio = float(input("Precio: "))
    producto = {"nombre": nombre, "categoria": categoria, "precio": precio}
    productos.append(producto)
    print(f"Producto {nombre} agregado.")

def consultar_productos():
    if not productos:
        print("No hay productos registrados.")
        return
    for i, producto in enumerate(productos):
        print(f"{i+1}. {producto}")

def actualizar_producto():
    consultar_productos()
    index = int(input("Seleccione el producto a actualizar: ")) - 1
    if 0 <= index < len(productos):
        productos[index]['nombre'] = input(f"Nuevo nombre ({productos[index]['nombre']}): ") or productos[index]['nombre']
        productos[index]['categoria'] = input(f"Nueva categoría ({productos[index]['categoria']}): ") or productos[index]['categoria']
        productos[index]['precio'] = float(input(f"Nuevo precio ({productos[index]['precio']}): ") or productos[index]['precio'])
        print("Producto actualizado.")
    else:
        print("Producto no encontrado.")

def eliminar_producto():
    consultar_productos()
    index = int(input("Seleccione el producto a eliminar: ")) - 1
    if 0 <= index < len(productos):
        productos.pop(index)
        print("Producto eliminado.")
    else:
        print("Producto no encontrado.")

# Reservas
def insertar_reserva():
    cliente = input("Nombre del cliente: ")
    promotor = input("Nombre del promotor: ")
    evento = input("Nombre del evento: ")
    zona = input("Zona reservada: ")
    fecha = input("Fecha (dd-mm-aaaa): ")
    reserva = {"cliente": cliente, "promotor": promotor, "evento": evento, "zona": zona, "fecha": fecha}
    reservas.append(reserva)
    print(f"Reserva para {cliente} creada.")

def consultar_reservas():
    if not reservas:
        print("No hay reservas registradas.")
        return
    
    tabla = PrettyTable()
    tabla.field_names = ["#", "Cliente", "Evento", "Zona", "Fecha", "Promotor"]

    for i, reserva in enumerate(reservas, start=1):
        tabla.add_row([
            i,
            reserva["cliente"],
            reserva["evento"],
            reserva["zona"],
            reserva["fecha"],
            reserva["promotor"]
        ])
    
    print(tabla)

def eliminar_reserva():
    consultar_reservas()
    index = int(input("Seleccione la reserva a eliminar: ")) - 1
    if 0 <= index < len(reservas):
        reservas.pop(index)
        print("Reserva eliminada.")
    else:
        print("Reserva no encontrada.")

# Ventas
def insertar_venta():
    producto = input("Nombre del producto vendido: ")
    cantidad = int(input("Cantidad: "))
    monto_total = float(input("Monto total: "))
    venta = {"producto": producto, "cantidad": cantidad, "monto_total": monto_total}
    ventas.append(venta)
    print("Venta registrada.")

def consultar_ventas():


# --- Reportes ---
def reporte_ventas():
    print("=== Reporte de Ventas ===")
    total = sum(venta['monto_total'] for venta in ventas)
    print(f"Total ventas: ${total:.2f}")
    consultar_ventas()

def reporte_inventario():
    print("=== Reporte de Inventario ===")
    consultar_productos()

def reporte_rendimiento_eventos():
    print("=== Reporte de Rendimiento de Eventos ===")
    eventos = {}
    for reserva in reservas:
        evento = reserva['evento']
        eventos[evento] = eventos.get(evento, 0) + 1
    for evento, count in eventos.items():
        print(f"Evento: {evento} - Reservas: {count}")

# --- Menú Principal ---
def menu_principal():
    while True:
        print("""
        === Bienvenido al sistema Santa Birra ===
        == Seleccione una opción ==
        1. Gestión de Clientes
        2. Gestión de Productos
        3. Gestión de Reservas
        4. Gestión de Ventas
        5. Generar Reportes
        6. Salir
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_crud_clientes()
        elif opcion == "2":
            menu_crud_productos()
        elif opcion == "3":
            menu_crud_reservas()
        elif opcion == "4":
            menu_crud_ventas()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

def menu_crud_clientes():
    while True:
        print("""
        === Gestión de Clientes - Santa Birra ===
        1. Insertar Cliente
        2. Consultar Clientes
        3. Actualizar Cliente
        4. Eliminar Cliente
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insertar_cliente()
        elif opcion == "2":
            consultar_clientes()
        elif opcion == "3":
            actualizar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menu_crud_productos():
    while True:
        print("""
        === Gestión de Productos - Santa Birra===
        1. Insertar Producto
        2. Consultar Productos
        3. Actualizar Producto
        4. Eliminar Producto
        5. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insertar_producto()
        elif opcion == "2":
            consultar_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def menu_crud_reservas():
    while True:
        print("""
        === Gestión de Reservas - Santa Birra ===
        1. Insertar Reserva
        2. Consultar Reservas
        3. Eliminar Reserva
        4. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insertar_reserva()
        elif opcion == "2":
            consultar_reservas()
        elif opcion == "3":
            eliminar_reserva()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def menu_crud_ventas():
    while True:
        print("""
        === Gestión de Ventas - Santa Birra ===
        1. Insertar Venta
        2. Consultar Ventas
        3. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            insertar_venta()
        elif opcion == "2":
            consultar_ventas()
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")

def menu_reportes():
    while True:
        print("""
        === Generar Reportes - Santa Birra ===
        1. Reporte de Ventas
        2. Reporte de Inventario
        3. Reporte de Rendimiento de Eventos
        4. Volver
        """)
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            reporte_ventas()
        elif opcion == "2":
            reporte_inventario()
        elif opcion == "3":
            reporte_rendimiento_eventos()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

# Iniciar el programa
menu_principal()
