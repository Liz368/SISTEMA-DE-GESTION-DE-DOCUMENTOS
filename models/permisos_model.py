from db.connection import crear_conexion
from psycopg2.extras import RealDictCursor
from psycopg2 import Error

def get_all_permisos():
    """Devuelve todos los permisos registrados en la tabla 'permisos'."""
    conn = crear_conexion()
    if not conn: return []
    
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT permiso_id, nombre, descripcion
            FROM permisos
            ORDER BY permiso_id;
        """)
        return cursor.fetchall()
    except Exception as e:
        print("Error en get_all_permisos:", e)
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_permisos_por_rol(rol_id):
    """Devuelve la lista de permisos asociados a un rol."""
    conn = crear_conexion()
    if not conn: return []

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT p.permiso_id, p.nombre, p.descripcion
            FROM permisos p
            INNER JOIN rol_permiso rp ON p.permiso_id = rp.permiso_id
            WHERE rp.rol_id = %s;
        """, (rol_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Error en get_permisos_por_rol:", e)
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def validar_permiso_usuario(usuario_id, permiso_nombre):
    """Verifica mediante el ID de usuario si cuenta con un permiso específico."""
    conn = crear_conexion()
    if not conn: return False

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT COUNT(*) AS existe
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.rol_id
            INNER JOIN rol_permiso rp ON r.rol_id = rp.rol_id
            INNER JOIN permisos p ON rp.permiso_id = p.permiso_id
            WHERE u.usuario_id = %s AND p.nombre = %s;
        """, (usuario_id, permiso_nombre))
        
        resultado = cursor.fetchone()
        return resultado["existe"] > 0 if resultado else False
    except Exception as e:
        print("Error en validar_permiso_usuario:", e)
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    

def asignar_permiso_a_rol(rol_id, permiso_id):
    """Asigna un permiso a un rol insertando en la tabla rol_permiso."""
    conn = crear_conexion()
    if not conn: return False

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rol_permiso (rol_id, permiso_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (rol_id, permiso_id))
        
        conn.commit()
        return True
    except Exception as e:
        print("Error en asignar_permiso_a_rol:", e)
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    

def revocar_permiso_de_rol(rol_id, permiso_id):
    """Revoca (elimina) un permiso asignado a un rol en la tabla rol_permiso."""
    conn = crear_conexion()
    if not conn: return False

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM rol_permiso
            WHERE rol_id = %s AND permiso_id = %s;
        """, (rol_id, permiso_id))
        
        conn.commit()
        return True
    except Exception as e:
        print("Error en revocar_permiso_de_rol:", e)
        if conn: conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()