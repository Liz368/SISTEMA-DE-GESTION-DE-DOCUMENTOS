from db.connection import crear_conexion
from psycopg2.extras import RealDictCursor


def get_all_roles():
    """
    Devuelve todos los roles como lista de diccionarios.
    """
    conn = crear_conexion()
    if not conn:
        return []

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT rol_id, nombre FROM roles ORDER BY rol_id")
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        return roles
    except Exception as e:
        print("Error en get_all_roles:", e)
        return []
    
def get_rol_nombre(rol_id):
    conn = crear_conexion()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM roles WHERE rol_id = %s", (rol_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print("Error en get_rol_nombre:", e)
        return None