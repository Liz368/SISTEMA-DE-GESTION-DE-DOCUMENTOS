from PyQt5.QtWidgets import  QMainWindow, QMainWindow
from ui_files.VentanaPrincipal_ui import Ui_VentanaPrincipal  # La clase generada por Qt Designer
from db.connection import crear_conexion
from msgboxes import msg_boxes
from ui_logic.ui_manager import VentanaUILogic
from controllers.usuario_controller import UsuarioPage
from controllers.rol_controller import RolPage
from models.permisos_model import validar_permiso_usuario
from PyQt5.QtWidgets import QApplication,QMenu, QAction
from PyQt5.QtCore import QObject, Qt



class VentanaPrincipal(QMainWindow, Ui_VentanaPrincipal): # Esta SI es una ventana
    def __init__(self, usuario_autenticado=None):
        super().__init__()

        self.setupUi(self)

        self.usuario_actual = usuario_autenticado

        #Efectos extras para ventana PRINCIPAL
        self.ui_logic = VentanaUILogic(self)
        self.ui_logic.aplicar_configuracion_inicial()
        # Llamada correcta al menú pasándole tu botón de usuario
        self.ui_logic.configurar_menu_usuario(self.btn_usuario)
        # Solo le pasamos el botón correspondiente de tu UI
        self.ui_logic.configurar_notificaciones(self.btn_notif)
        

        self.configurar_accesos_segun_permisos()

        #Controller USUARIO PAGE
        self.pagina_usuario = UsuarioPage(self)
        self.pagina_usuario.cargar_tabla_usuarios()  

        #Controller ROL PAGE
        self.pagina_rol = RolPage(self)
        self.pagina_rol.cargar_tabla_roles()
   

    def configurar_accesos_segun_permisos(self):
        """
        Oculta de la vista los botones cuyos permisos no pertenezcan al usuario.
        """

        # Si por alguna razón no hay usuario autenticado, cerramos seguridad por precaución
        if not self.usuario_actual:
            print("Advertencia: No se detectó ningún usuario autenticado.")
            return

        # CORRECCIÓN EXTRA: Extraemos el ID numérico del diccionario del usuario
        u_id = self.usuario_actual.get('usuario_id')

        if not u_id:
            print("Error: El usuario actual no cuenta con un 'usuario_id' válido.")
            return

       # ---------------------------------------------------------------------
        # VALIDACIÓN DE PERMISOS (Sección por Sección)
        # ---------------------------------------------------------------------
        
        # 1. 
        self.btn_rol.setVisible(True) # <- Forzamos a que aparezca primero
        if not validar_permiso_usuario(u_id, 'menu_roles'):
            self.btn_rol.setVisible(False) 
            
        # 2. Menú de Usuarios
        self.btn_user.setVisible(True) # <- Forzamos a que aparezca primero
        if not validar_permiso_usuario(u_id, 'menu_usuarios'):
            self.btn_user.setVisible(False)

        # 3. Menú de Documentos
        self.btn_doc.setVisible(True) # <- Forzamos a que aparezca primero
        if not validar_permiso_usuario(u_id, 'menu_documentos'):
            self.btn_doc.setVisible(False)

   


   
    
