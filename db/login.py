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
             
import sys
from PyQt5.QtWidgets import QApplication
# Importamos el controlador (MainWindow) que acabamos de completar
from controllers.login_controller import  VentanaPrincipal


def main():
    # 1. Crear la instancia de la aplicación
    # sys.argv permite que la app reconozca argumentos de línea de comandos
    app = QApplication(sys.argv)

    # 2. Instanciar el controlador (la ventana)
    ventana_login = VentanaPrincipal()
    

    # 3. Mostrar la ventana al usuario
    ventana_login.show()
    

    # 4. Ejecutar el bucle de eventos (mantiene la ventana abierta)
    # sys.exit asegura que el proceso termine limpiamente al cerrar la app
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 