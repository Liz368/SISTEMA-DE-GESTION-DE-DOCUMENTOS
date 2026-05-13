from db.connection import crear_conexion

#Buscar en la base de datos para que pueda ingresar en el login

def validar_usuario(usuario, password):
    conn = crear_conexion()
    if conn is None:
        return None
    
    # Buscamos al usuario que coincida con nombre y pass
    # Importante: En producción usa hashing para el pass
    sql = """SELECT u.usuario_id, u.username, u.nombres, r.nombre, u.estado
            FROM usuarios u 
            JOIN roles r ON u.rol_id = r.rol_id 
            WHERE u.username = %s AND u.password = %s AND u.estado = True"""
    cur = None

    try:
        cur = conn.cursor()
        cur.execute(sql, (usuario, password))
        resultado = cur.fetchone() # Devuelve la fila si existe, o None si no
        print(f"Resultado de la DB: {resultado}")
        return resultado
    except Exception as e:
        print(f"Error en la consulta de login: {e}")
        return None
    finally:
        cur.close()
        conn.close()
             