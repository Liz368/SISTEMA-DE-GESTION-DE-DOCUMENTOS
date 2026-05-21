import sys
from PyQt5.QtWidgets import QApplication
# Importamos el controlador (MainWindow) que acabamos de completar
from controllers.ventanaPrincipal_controller import   VentanaPrincipal


def main():
    # 1. Crear la instancia de la aplicación
    # sys.argv permite que la app reconozca argumentos de línea de comandos
    app = QApplication(sys.argv)

    # 2. Instanciar el controlador (la ventana)
    ventana_login = VentanaPrincipal()
    

    # 3. Mostrar la ventana al usuario
    ventana_login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 