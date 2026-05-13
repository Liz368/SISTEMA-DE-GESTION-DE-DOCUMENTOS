import sys
from PyQt5.QtWidgets import QApplication
# Importamos el controlador (MainWindow) que acabamos de completar
from controllers.login_controller import Login


#import qdarkstyle

def main():
    # 1. Crear la instancia de la aplicación
    # sys.argv permite que la app reconozca argumentos de línea de comandos
    app = QApplication(sys.argv)

    # 2. Instanciar el controlador (la ventana)
    ventana_login = Login()
    

    # 3. Mostrar la ventana al usuario
    ventana_login.show()
    

    # 4. Ejecutar el bucle de eventos (mantiene la ventana abierta)
    # sys.exit asegura que el proceso termine limpiamente al cerrar la app
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 