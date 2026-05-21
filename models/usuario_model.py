from db.connection import crear_conexion
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import bcrypt   # Para manejar contraseñas encriptadas


# =====================================================================
# METODOS DE SEGURIDAD 
# =====================================================================

def generar_hash(password_input: str) -> str:
    """Encripta la contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_input.encode('utf-8'), salt).decode('utf-8')

def verificar_password(password_input: str, password_hash: str) -> bool:
    """Verifica si la contraseña ingresada coincide con el hash guardado"""
    return bcrypt.checkpw(password_input.encode('utf-8'), password_hash.encode('utf-8'))

# =====================================================================
# FUNCIONES DE BASE DE DATOS SQL
# =====================================================================

def insert(data):
    conn = crear_conexion()
    
    query = "INSERT INTO usuarios (nombres, apellidos, username, password, rol_id, estado, fecha_inicio, fecha_fin) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cursor = None 
    try:
        cursor = conn.cursor()
        cursor.execute(query, list(data.values()))
        conn.commit()
        return True
        
    except Error as err:
        print(f"Error al insertar funcion: {err}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update(_id, data):
    conn = crear_conexion()

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
            data['nombres'],
            data['apellidos'],
            data['username'],
            data['password'],
            data['rol_id'],
            data['estado'],
            data['fecha_inicio'],
            data['fecha_fin'],
            _id
        ]

        print("SQL placeholders:", query.count("%s"))
        print("Valores:", len(valores))
        cursor.execute(query, valores)
        conn.commit()
        print("Usuario actualizado con éxito")
        return cursor.rowcount > 0
    except Error as err:
        print(f"Error al actualizar: {err}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_por_username(username):
    """
    Busca un usuario por su nombre de usuario en la tabla usuarios,
    incluyendo el rol asociado.
    Devuelve un diccionario con los datos o None si no existe.
    """
    conn = crear_conexion()
    if not conn:
        return None

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT u.*, r.nombre AS rol_nombre
            FROM usuarios u
            LEFT JOIN roles r ON u.rol_id = r.rol_id
            WHERE u.username = %s
        """, (username,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    except Exception as e:
        print("Error en buscar_por_username:", e)
        return None 

def get_permisos_por_rol(rol_id):
    """
    Devuelve la lista de permisos asociados a un rol.
    Retorna una lista de diccionarios con los nombres de los permisos.
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
        """, (rol_id,))
        permisos = cursor.fetchall()
        cursor.close()
        conn.close()
        return permisos
    except Exception as e:
        print("Error en get_permisos_por_rol:", e)
        return []


def get_all():
    """
    Devuelve todos los usuarios como lista de diccionarios.
    """
    conn = crear_conexion()
    if not conn:
        return []

    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        print("Error en get_all:", e)
        return []


def obtener_usuarios_activos():
    """Devuelve únicamente los usuarios cuyo estado es 1 (Activo) """
    conn = crear_conexion()
    cursor = None
    
    # 2. En MySQL de XAMPP filtramos por 1 en lugar de TRUE
    query = "SELECT * FROM usuarios WHERE estado = 1;"
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        return cursor.fetchall()  
        
    except Error as err:
        print(f"Error al obtener usuarios activos: {err}")
        return [] # Devolvemos una lista vacía si hay un error
        
    finally:
        # 3. Cerramos los recursos de forma segura
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def buscar_por_id(usuario_id):
    conn = crear_conexion()
    query = """
        SELECT usuario_id, nombres, apellidos, username, rol_id, estado, fecha_inicio, fecha_fin
        FROM usuarios
        WHERE usuario_id = %s
    """
    try:
        cur = conn.cursor()
        cur.execute(query, (usuario_id,))
        row = cur.fetchone()
        if row:
            return {
                'usuario_id': row[0],
                'nombres': row[1],
                'apellidos': row[2],
                'username': row[3],
                'rol_id': row[4],
                'estado': row[5],
                'fecha_inicio': row[6],
                'fecha_fin': row[7],
            }
        return None
    finally:
        cur.close()
        conn.close()
