import mensajes as msj
from inputHelper import *
from outputHelper import *
from validadorFK import *

def crear_miembro(db):
    cedula = pedirCedula("Cédula del empleado: ")
    if validar_clave_foranea(db, "MEMBER", "Mem_ID", cedula):
        printMensajeIngresoExistente()
        return

    nombre = pedirNombre("Nombre del empleado: ")
    apellido = pedirApellido("Apellido del empleado: ")
    experiencia = pedirEnteroPositivo("Experiencia del empleado en años: ")
    rol = pedirRol()

    conection = db.cursor()
    tupla = (cedula, nombre, apellido, experiencia)
    sql = "INSERT INTO MEMBER (Mem_ID, Mem_FName, Mem_LName, Mem_Experience) VALUES (%s, %s, %s, %s)" 
    conection.execute(sql,tupla)
    db.commit()

    ingresarPorRol(db, conection, rol, cedula)

    printIngresoExitoso()

  
def pedirRol():
    roles = ["G","P","S","M"]
    print("\nOpciones de rol.\nG - Guardia.\nP - Promotor.\nS - Vendedor\nM - Manager")
    rol = input("Rol: ").upper()
    while rol not in roles:
        print("Ingrese un rol válido.")
        rol = input("Rol: ").upper()
    print()
    return rol

def ingresarPorRol(db, conection, rol, cedula):
    if rol == "G":
        insertar_miembro(db, conection, "GUARD", cedula)

    elif rol == "P":
        comision = pedirDecimalPositivo("Comisión del promotor: ")
        manager = pedirManager(db)

        sql = "INSERT INTO PROMOTOR (Mem_ID, Prom_com, Mem_Man) VALUES (%s,%s,%s)"
        tupla = (cedula, comision, manager)
        conection.execute(sql, tupla)
        db.commit()

    elif rol == "S":
        insertar_miembro(db, conection, "SELLER", cedula)

    else:
        insertar_miembro(db, conection, "MANAGER", cedula)

def insertar_miembro(db, conection, miembro, cedula):
    query = "INSERT INTO {} (Mem_ID) VALUES (%s)".format(miembro)
    tupla = (cedula,)
    conection.execute(query, tupla)
    db.commit()

def pedirManager(db):
    opcion = pedirEntreDosOpciones("Opciones para Manager", "No asignar Manager", "Ingresar Manager")
    if opcion == 1:
        return None
    else:
        consultar_empleadosPorRol(db, "MANAGER")
        manager = pedirCedula("Cédula del manager: ")
        while not validar_clave_foranea(db, "MEMBER", "Mem_ID", manager):
            printMensajeErrorFK()
            manager = pedirCedula("Cédula del manager: ")
        return manager

def obtenerRol(db, cedula):
    conection = db.cursor()
    conection.execute("SELECT * FROM MEMBER WHERE Mem_ID=%s", (cedula,))
    datos = conection.fetchone()
    cedula = datos[0]
    rol = None

    if validar_clave_foranea(db, "GUARD", "Mem_ID", cedula):
        rol = "Guardia"
    elif validar_clave_foranea(db, "PROMOTOR", "Mem_ID", cedula):
        rol = "Promotor"
    elif validar_clave_foranea(db, "SELLER", "Mem_ID", cedula):
        rol = "Vendedor"
    else:
        rol = "Manager"
    return rol

def consultar_empleados(db):
    conection = db.cursor()
    conection.execute("SELECT * FROM MEMBER")
    datos = conection.fetchall()
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        apellido = fila[2]
        experiencia = fila[3]
        print(f"Cédula: {cedula}, Nombre: {nombre}, Apellido: {apellido}, Experiencia: {experiencia}")

#Consulta empleados de un rol específico
def consultar_empleadosPorRol(db, rol):
    conection = db.cursor()
    conection.execute("SELECT * FROM MEMBER WHERE Mem_ID IN (SELECT Mem_ID FROM {})".format(rol))
    datos = conection.fetchall()
    for fila in datos:
        cedula = fila[0]
        nombre = fila[1]
        apellido = fila[2]
        experiencia = fila[3]
        print(f"Cédula: {cedula}, Nombre: {nombre}, Apellido: {apellido}, Experiencia: {experiencia}, Rol: {rol}")

def consultarPorRol(db):

    rol = pedirRol()

    if rol == "G":
        consultar_empleadosPorRol(db, "GUARD")

    elif rol == "P":
        consultar_empleadosPorRol(db, "PROMOTOR")

    elif rol == "S":
        consultar_empleadosPorRol(db, "SELLER")

    else:
        consultar_empleadosPorRol(db, "MANAGER")

def consultarEmpleadosPorRolBucle(db):
    inputUsuario = pedirSiONo("¿Desea consultar empleados? Presione s para continuar o n para salir: ")
    while inputUsuario == "s":
        consultarPorRol(db)
        inputUsuario = pedirSiONo("¿Desea consultar empleados? Presione s para continuar o n para salir: ")

def actualizar_empleado(db):
    conection = db.cursor()
    cedula = pedirCedula("Cédula del empleado: ")
    if not validar_clave_foranea(db, "MEMBER", "Mem_ID", cedula):
        printMensajeErrorFK()
        return
    
    experiencia = pedirEnteroPositivo("Experiencia en años actualizada: ")

    query = "UPDATE MEMBER SET Mem_experience=%s WHERE Mem_ID=%s"
    values = (experiencia, cedula)
            
    conection.execute(query, values)
    db.commit()
    printActualizacionExitosa()

def eliminar_empleado(db):
    conection = db.cursor()
    cedula = pedirCedula("Cédula del empleado: ")

    query = "DELETE FROM MEMBER WHERE Mem_ID=%s"
    values = (cedula, )
            
    conection.execute(query, values)
    db.commit()
    if conection.rowcount == 0:
        printMensajeErrorFK()
    else:
        printEliminacionExitosa()


def menu_crud_empleados(db):
    while True:
        print(msj.opcionesEmpleado)
        opcion = input("Seleccione una opción: ")  
        if opcion == "1":
            crear_miembro(db)
        elif opcion == "2":
            consultar_empleados(db)
        elif opcion == "3":
            consultarEmpleadosPorRolBucle(db)
        elif opcion == "4":
            consultar_empleados(db)
            actualizar_empleado(db) 
        elif opcion == "5":
            consultar_empleados(db)
            eliminar_empleado(db)
        elif opcion == "6":
            break
        else:
            print(msj.opcionesError)
