from db.connection import crear_conexion
from psycopg2.extras import RealDictCursor
from psycopg2 import Error
import bcrypt

# =====================================================================
# METODOS DE SEGURIDAD 
# =====================================================================

def generar_hash(password_input: str) -> str:
    """Encripta la contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_input.encode('utf-8'), salt).decode('utf-8')

def verificar_password(password_ingresada: str, password_hash: str) -> bool:
    """
    Compara la contraseña en texto plano con el hash de la base de datos.
    """
    try:
        return bcrypt.checkpw(
            password_ingresada.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False      
# =====================================================================
# FUNCIONES DE BASE DE DATOS SQL
# =====================================================================

def insert(data):
    """Inserta un nuevo usuario asegurando el orden correcto de las columnas"""
    conn = crear_conexion()
    if not conn:
        return False
        
    query = """
        INSERT INTO usuarios (nombres, apellidos, username, password, rol_id, estado, fecha_inicio, fecha_fin) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = None 
    try:
        cursor = conn.cursor()
        # CORRECCIÓN: Mapeo explícito para evitar datos cruzados
        valores = [
            data.get('nombres'), data.get('apellidos'), data.get('username'),
            data.get('password'), data.get('rol_id'), data.get('estado'),
            data.get('fecha_inicio'), data.get('fecha_fin')
        ]
        cursor.execute(query, valores)
        conn.commit()
        return True
    except Error as err:
        print(f"Error al insertar usuario: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def update(_id, data):
    """Actualiza los datos de un usuario por su ID"""
    conn = crear_conexion()
    if not conn:
        return False

    query = """ 
        UPDATE usuarios SET 
            nombres = %s,
            apellidos = %s,
            username = %s,
            password = %s,
            rol_id = %s,
            estado = %s,
            fecha_inicio = %s,
            fecha_fin = %s 
        WHERE usuario_id = %s
    """
    cursor = None
    try:
        cursor = conn.cursor()
        valores = [
            data.get('nombres'), data.get('apellidos'), data.get('username'),
            data.get('password'), data.get('rol_id'), data.get('estado'),
            data.get('fecha_inicio'), data.get('fecha_fin'), _id
        ]
        cursor.execute(query, valores)
        conn.commit()
        return cursor.rowcount > 0
    except Error as err:
        print(f"Error al actualizar usuario: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def buscar_por_username(username):
    """Busca un usuario por su username para el Login, incluyendo su rol"""
    conn = crear_conexion()
    if not conn:
        return None

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT u.*, r.nombre AS rol_nombre
            FROM usuarios u
            LEFT JOIN roles r ON u.rol_id = r.rol_id
            WHERE u.username = %s
        """, (username,))
        return cursor.fetchone()
    except Exception as e:
        print("Error en buscar_por_username:", e)
        return None 
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_all():
    """Devuelve la lista completa de usuarios con sus roles unidos por INNER JOIN"""
    conn = crear_conexion()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                u.usuario_id, u.nombres, u.apellidos, u.username,
                u.estado, u.fecha_inicio, u.rol_id,
                r.nombre AS rol_nombre
            FROM usuarios u
            INNER JOIN roles r ON u.rol_id = r.rol_id;
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("Error en get_all usuarios:", e)
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def obtener_usuarios_activos():
    """Devuelve únicamente los usuarios cuyo estado es TRUE (Activos) en PostgreSQL"""
    conn = crear_conexion()
    if not conn:
        return []
        
    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # CORRECCIÓN: Filtramos usando TRUE nativo de PostgreSQL
        cursor.execute("SELECT * FROM usuarios WHERE estado = TRUE;")
        return cursor.fetchall()  
    except Error as err:
        print(f"Error al obtener usuarios activos: {err}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def get_usuario_by_id(usuario_id):
    """Busca un usuario por su ID y lo devuelve directamente como diccionario"""
    conn = crear_conexion()
    if not conn:
        return None
        
    cursor = None
    query = """
        SELECT usuario_id, nombres, apellidos, username, rol_id, estado, fecha_inicio, fecha_fin
        FROM usuarios
        WHERE usuario_id = %s
    """
    try:
        # OPTIMIZACIÓN: Al usar RealDictCursor, el return se vuelve directo y corto
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()
    except Exception as e:
        print("Error en get_usuario_by_id:", e)
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()