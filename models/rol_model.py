from db.connection import crear_conexion
from psycopg2.extras import RealDictCursor
from psycopg2 import Error


def update(_id, data):
    conn = crear_conexion()

    query = """
        UPDATE roles SET
            nombre = %s,
            descripcion = %s
        WHERE rol_id = %s
    """

    cursor = None
    try:
        cursor = conn.cursor()
        valores = [data.get('nombre'), data.get('descripcion'), _id]
        
        cursor.execute(query, valores)
        conn.commit()
        return True
    except Error as err:
        print(f"Error al actualizar : {err}")
        if conn:
            conn.rollback()
            return False
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            cursor.close()



def get_rol_nombre(nombre_rol):
    """
    Busca si existe un rol por su TEXTO (nombre). Útil para validar duplicados en formularios.
    """
    conn = crear_conexion()
    if not conn:
        return None
        
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # Buscamos de forma exacta por el nombre enviado
        cursor.execute("SELECT * FROM roles WHERE nombre = %s", (nombre_rol,))
        result = cursor.fetchone()
        return result if result else None # Devuelve el diccionario del rol o None si no existe
    except Exception as e:
        print("Error en get_rol_nombre:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_rol_by_id(rol_id):
    """
    Busca un rol específico por su número ID numérico.
    """
    conn = crear_conexion()
    if not conn:
        return None
        
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT rol_id, nombre, descripcion FROM roles WHERE rol_id = %s"
        cursor.execute(query, (rol_id,))
        row = cursor.fetchone()
        return row if row else None # Devuelve el diccionario directo {'rol_id': X, 'nombre': Y...}
    except Exception as e:
        print("Error en get_rol_by_id:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_roles():
    """
    Devuelve todos los roles como lista de diccionarios para rellenar tablas o comboboxes.
    """
    conn = crear_conexion()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT rol_id, nombre, descripcion FROM roles ORDER BY rol_id")
        roles = cursor.fetchall()
        return roles
    except Exception as e:
        print("Error en get_all_roles:", e)
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_roles():
    """
    Devuelve todos los roles como lista de diccionarios.
    """
    conn = crear_conexion()
    if not conn:
        return []

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT rol_id, nombre, descripcion FROM roles ORDER BY rol_id")
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        return roles
    except Exception as e:
        print("Error en get_all_roles:", e)
        return []
    
    

def guardar_permisos_rol(rol_id, lista_permisos):
    """Borra los permisos anteriores e inserta los nuevos seleccionados en la UI"""
    conn = crear_conexion()
    if not conn: 
        return False
        
    cursor = None
    try:
        cursor = conn.cursor()
        # 1. Borramos las relaciones viejas en 'rol_permiso'
        cursor.execute("DELETE FROM rol_permiso WHERE rol_id = %s;", (rol_id,))
        
        # 2. Si el usuario marcó checkboxes, los insertamos en lote (bulk insert)
        if lista_permisos:
            # CORRECCIÓN: Buscamos el permiso_id usando la columna 'nombre' de tu tabla permisos
            query = """
                INSERT INTO rol_permiso (rol_id, permiso_id)
                VALUES (%s, (SELECT permiso_id FROM permisos WHERE nombre = %s));
            """
            # Preparamos la lista de tuplas [(rol_id, 'permiso1'), (rol_id, 'permiso2'), ...]
            valores = [(rol_id, p) for p in lista_permisos]
            cursor.executemany(query, valores)
            
        conn.commit()
        return True
    except Error as err:
        print(f"Error al guardar permisos en la BD: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def listar_permisos_de_rol(rol_id):
    """
    Lista todos los permisos asociados a un rol.
    Retorna una lista de diccionarios con permiso_id, nombre y descripcion.
    """
    conn = crear_conexion()
    if not conn:
        return []

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT p.permiso_id, p.nombre, p.descripcion
            FROM permisos p
            INNER JOIN rol_permiso rp ON p.permiso_id = rp.permiso_id
            WHERE rp.rol_id = %s
            ORDER BY p.permiso_id;
        """, (rol_id,))
        permisos = cursor.fetchall()
        cursor.close()
        conn.close()
        return permisos
    except Exception as e:
        print("Error en listar_permisos_de_rol:", e)
        return []
    
