from PyQt5.QtWidgets import QWidget, QMainWindow
from views.login_ui import Login
from ui_files.principal_ui import Ui_VentanaPrincipal
from msgboxes import msg_boxes
from db.login import validar_usuario
from PyQt5.QtWidgets import QLineEdit, QAction
from PyQt5.QtGui import QIcon
# Importamos la herramienta de estilos


# --- CLASES DE LAS VENTANAS DE DESTINO ---

class VentanaPrincipal(QMainWindow, Ui_VentanaPrincipal):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        
# --- CONTROLADOR DE LOGIN ---

class Login(QWidget, Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Aplicar estilo al login también (opcional)

        self.btn_ingresar.setShortcut("Return")
        self.input_user.setFocus()

        self.input_user.returnPressed.connect(self.autentica)
        self.input_pass.returnPressed.connect(self.autentica)
        self.btn_ingresar.clicked.connect(self.autentica)

         # 1. Creamos el objeto QAction (el ojo)
        # No necesitas ponerlo en el Designer, esto lo crea en memoria
        self.ojo_action = QAction(self)
        
        # 2. Le ponemos el icono inicial (ojo cerrado/ocultar)
        self.ojo_action.setIcon(QIcon(""))
        
        # 3. ¡Aquí está el truco! Lo metemos dentro del TXT de password
        # TrailingPosition significa "al final" (derecha)
        self.input_pass.addAction(self.ojo_action, QLineEdit.TrailingPosition)
        
        # 4. Lo conectamos a una función para que haga algo al hacerle clic
        self.ojo_action.triggered.connect(self.toggle_pass)

    # 5. La función que cambia todo
    def toggle_pass(self):
            if self.input_pass.echoMode() == QLineEdit.Password:
                    # Si está oculto, lo mostramos
                    self.input_pass.setEchoMode(QLineEdit.Normal)
                    self.ojo_action.setIcon(QIcon(":/res_icon/icons/eye.svg"))
            else:
                    # Si se ve, lo ocultamos
                    self.input_pass.setEchoMode(QLineEdit.Password)
                    self.ojo_action.setIcon(QIcon(":/res_icon/icons/eye-off.svg"))


    def autentica(self):
        usuario_input = self.input_user.text().strip().upper()
        password_input = self.input_pass.text().strip()

        if not usuario_input or not password_input:
            msg_boxes.error_msgbox("Error", "Por favor, introduzca todos los datos.")
            return
        
        datos_usuario = validar_usuario(usuario_input, password_input)

        if datos_usuario:
            usuario_id, username, nombres, nombre_rol, activo = datos_usuario

            if activo == 0:
                msg_boxes.error_msgbox("Cuenta Inactiva", "Tu usuario está desactivado.")
                return

            print(f"Acceso correcto: {nombres} | Rol: {nombre_rol}")

            # 3. NAVEGACIÓN LIMPIA
            if nombre_rol == "ADMIN":
                self.nueva_ventana = VentanaPrincipal()
            elif nombre_rol == "USUARIO":
                self.nueva_ventana = VentanaPrincipal()
            else:
                msg_boxes.error_msgbox("Error", "Rol no reconocido.")
                return

            self.nueva_ventana.showMaximized()
            self.close()

        else:
            msg_boxes.error_msgbox("Error", "Credenciales incorrectas.")