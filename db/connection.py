import psycopg2
from psycopg2 import OperationalError

# Configuración de la base de datos
config = {
    'dbname': 'DOC-PRUEBA',   # Nombre de tu base de datos
    'user': 'postgres',       # Usuario de PostgreSQL
    'password': '63219308',           # Contraseña (si tienes)
    'host': 'localhost',
    'port': 5432              # Puerto por defecto PostgreSQL
}

def crear_conexion():
    conn = None
    try:
        conn = psycopg2.connect(**config)
        print("DEBUG: Conexión exitosa a PostgreSQL")
    except OperationalError as err:
        print(f"Error al conectar a la base de datos: {err}")
    return conn
