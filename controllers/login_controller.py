from PyQt5.QtWidgets import QWidget, QAction, QLineEdit
from PyQt5.QtGui import QIcon
from views.login_ui import Login
from models.usuario_model import buscar_por_username, verificar_password, get_permisos_por_rol
from msgboxes import msg_boxes
from controllers.ventanaPrincipal_controller import VentanaPrincipal

class LoginController(QWidget, Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_ingresar.setShortcut("Return")
        self.input_user.setFocus()

        # Configuración del ojo de la contraseña
        self.ojo_action = QAction(self)
        self.ojo_action.setIcon(QIcon(":/res_icon/icons/eye-off.svg"))
        self.input_pass.addAction(self.ojo_action, QLineEdit.TrailingPosition)

        self.ojo_action.triggered.connect(self.mostrar_ocultar_pass)
        self.btn_ingresar.clicked.connect(self.autentica)
        self.input_pass.returnPressed.connect(self.autentica)

    def mostrar_ocultar_pass(self):
        if self.input_pass.echoMode() == QLineEdit.Password:
            self.input_pass.setEchoMode(QLineEdit.Normal)
            self.ojo_action.setIcon(QIcon(":/res_icon/icons/eye.svg"))
        else:
            self.input_pass.setEchoMode(QLineEdit.Password)
            self.ojo_action.setIcon(QIcon(":/res_icon/icons/eye-off.svg"))

    def autentica(self):
        user_text = self.input_user.text().strip().upper()
        pass_text = self.input_pass.text().strip()

        if not user_text or not pass_text:
            msg_boxes.error_msgbox("Error", "Complete los campos.")
            return

        try:
            usuario = buscar_por_username(user_text)
            print("DEBUG: Usuario encontrado:", usuario)

            if usuario and verificar_password(pass_text, usuario.get('password')):
                if usuario.get('estado') == 0:
                    msg_boxes.error_msgbox("Error", "Usuario inactivo.")
                    return

                #Traer rolo y permisos
                rol = usuario.get('rol_nombre')
                print("DEBUG: Rol del usuario:", rol)
                permisos = get_permisos_por_rol(usuario.get('rol_id'))
                usuario['permisos'] = permisos
        
                self.abrir_principal(usuario)
            else:
                msg_boxes.error_msgbox("Error", "Credenciales incorrectas.")
        except Exception as e:
            msg_boxes.error_msgbox("Error de Sistema", f"No se pudo completar la autenticacion.\nDetalle: {e}")
            print("DEBUG: Excepción en autentica:", e)

    def abrir_principal(self, usuario):
        print("DEBUG: Entrando a abrir_principal con:", usuario)
        self.principal = VentanaPrincipal(usuario_autenticado=usuario)
        self.principal.showMaximized()
        print("DEBUG: Ventana principal mostrada")
        self.hide()  # ocultar login en lugar de cerrar
