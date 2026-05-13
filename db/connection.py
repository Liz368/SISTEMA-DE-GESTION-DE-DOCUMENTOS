import psycopg2
#conexion con la base de datos Postgres
config = {
    'user' : 'postgres',
    'password' : '63219308',
    'host' : 'localhost',
    'database' : 'DOC-PRUEBA'

}

def crear_conexion():
    conn = None
    try:
        conn = psycopg2.connect(**config)
    except Exception as err:
        print("Erro al crear la conexion funcion: {err}")
    return conn
