def validar_clave_foranea(db, tabla, columna, valor):
    conection = db.cursor()
    # Consulta para verificar que el valor existe en la tabla referenciada
    query = f"SELECT COUNT(*) FROM {tabla} WHERE {columna} = %s"
    conection.execute(query, (valor,))
    return conection.fetchone()[0] > 0

