from PyQt5.QtWidgets import  QMainWindow
from ui_files.VentanaPrincipal_ui import Ui_VentanaPrincipal  # La clase generada por Qt Designer
from db.connection import crear_conexion
from msgboxes import msg_boxes
from ui_logic.ui_manager import VentanaUILogic
from controllers.usuario_controller import UsuarioPage



class VentanaPrincipal(QMainWindow, Ui_VentanaPrincipal): # Esta SI es una ventana
    def __init__(self, usuario_autenticado=None):
        super().__init__()

        self.setupUi(self)

        self.usuario_actual = usuario_autenticado

        #Efectos extras para ventana PRINCIPAL
        self.ui_logic = VentanaUILogic(self)
        self.ui_logic.aplicar_configuracion_inicial()

        #Controller USUARIO PAGE
        self.pagina_usuario = UsuarioPage(self)
        self.pagina_usuario.cargar_tabla_usuarios()  
        
        
    
      
