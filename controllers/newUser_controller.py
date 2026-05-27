from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QEvent 
from ui_files.addUser_ui import Ui_DialogAgregar 
from models.usuario_model import get_all,buscar_por_username, insert, generar_hash
from models.rol_model import get_all_roles
from msgboxes import msg_boxes 
from datetime import date

class newUser(QDialog, Ui_DialogAgregar):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        #Lenar comobo roles desde la base de datos
        self.cargar_roles()

        # Conexión de eventos
        self.btn_guardar.clicked.connect(self.create)
        self.btn_guardar.setShortcut("Return")
        
        for campo in (self.input_nameUser, self.input_pass, self.input_nombre, self.input_apellido):
            campo.installEventFilter(self)

        self.dateEdit.setDate(date.today())

    def cargar_roles(self):
        roles = get_all_roles()
        self.comboBox_rol.clear()
        # Agregar opción predeterminada
        self.comboBox_rol.addItem("-- Seleccione un Rol --", None)
        for rol in roles:
            # Texto visible = nombre, userData = rol_id
            self.comboBox_rol.addItem(rol['nombre'], rol['rol_id'])

        # Seleccionar la opción predeterminada al abrir
        self.comboBox_rol.setCurrentIndex(0)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.create()
            return True
        return super().eventFilter(obj, event)
    
    def verificar_inputs(self):
        username = self.input_nameUser.text().strip().upper()
        password = self.input_pass.text().strip()

        rol_id =  self.comboBox_rol.currentData()

        #Check de los inputs username, pass y rol
        if not username or not password or rol_id is None:
            msg_boxes.error_msgbox("Campos Obligatorios", "El usuario, la contraseña y el rol no pueden estar vacíos.")
            return False
        return True


    # Asegúrate de importar tus funciones de base de datos al inicio de este archivo:
    # from .tu_archivo_bd import buscar_por_username, insert, desactivar_usuario

    def create(self):
        if not self.verificar_inputs():
            return

        # 1. Capturamos los datos de los componentes de PyQt5
        username = self.input_nameUser.text().strip().upper()
        password = self.input_pass.text().strip()
        nombres = self.input_nombre.text().strip()
        apellidos = self.input_apellido.text().strip()
        
        estado = self.checkBox_activo.isChecked()
        f_inicio = self.dateEdit.date().toPyDate() or date.today()

        rol_id =  self.comboBox_rol.currentData()

        try:
            # 2. VALIDACIÓN: Buscamos si el username ya existe usando nuestra nueva función
            usuario_existente = buscar_por_username(username)
            if usuario_existente:
                msg_boxes.error_msgbox("Validación", f"El nombre de usuario '{username}' ya se encuentra registrado.")
                return

            # 3. ARMAMOS EL DICCIONARIO: En el orden exacto que espera tu función insert()
            data = {
                'nombres': nombres,
                'apellidos': apellidos,
                'username': username,
                'password': generar_hash(password), 
                'rol_id': rol_id,
                'estado': estado,
                'fecha_inicio': f_inicio,
                'fecha_fin' : None
            }

            # 4. EJECUTAMOS LA INSERCIÓN: Pasamos el diccionario completo
            if insert(data):
                msg_boxes.correct_msgbox("Éxito", f"El usuario '{username}' ha sido creado correctamente.")
                self.limpiar_formulario()
                
                # Avisamos a Qt que cerramos con éxito para que la ventana principal se entere
                self.accept() 
            else:
                msg_boxes.error_msgbox("Error", "No se pudo registrar el usuario en la base de datos.")

        except Exception as e:
            msg_boxes.error_msgbox("Error de Base de Datos", f"Ocurrió un error inesperado.\nDetalle: {e}")


    def limpiar_formulario(self):
        """Limpia todos los campos de la interfaz para un nuevo registro"""
        for campo in (self.input_nameUser, self.input_pass, self.input_nombre, self.input_apellido):
            campo.clear()
        self.checkBox_activo.setChecked(True)
        self.comboBox_rol.setCurrentIndex(0)


