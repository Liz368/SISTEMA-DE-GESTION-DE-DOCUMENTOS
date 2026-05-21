from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QEvent 
from ui_files.editUser_ui import  Ui_DialogEditar
from models.usuario_model import buscar_por_username, update, generar_hash, buscar_por_id 
from models.rol_model import get_all_roles
from msgboxes import msg_boxes 
from datetime import date

class editUser(QDialog, Ui_DialogEditar):
    
    def __init__(self, parent=None, usuario_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.usuario_id = usuario_id

        #Lenar combo roles desde la base de datos
        self.cargar_roles()
        if usuario_id:
            self.cargar_datos_usuario(usuario_id)

        # Conexión de eventos
        self.btn_guardar.clicked.connect(self.edit)
        self.btn_guardar.setShortcut("Return")
        
        for campo in (self.input_nameUser, self.input_pass, self.input_nombre, self.input_apellido):
            campo.installEventFilter(self)

        self.dateEdit.setDate(date.today())

    def cargar_datos_usuario(self, usuario_id):
        usuario = buscar_por_id(usuario_id)
        if usuario:
            self.input_nameUser.setText(usuario['username'])
            self.input_nombre.setText(usuario['nombres'])
            self.input_apellido.setText(usuario['apellidos'])
            self.checkBox_activo.setChecked(usuario['estado'])
            self.dateEdit.setDate(usuario['fecha_inicio'])

            # Seleccionar rol correcto
            index = self.comboBox_rol.findData(usuario['rol_id'])
            if index >= 0:
                self.comboBox_rol.setCurrentIndex(index)

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
            self.btn_guardar.click()
            return True
        return super().eventFilter(obj, event)
    
    def verificar_inputs(self, require_password=True):
        username = self.input_nameUser.text().strip().upper()
        password = self.input_pass.text().strip()

        rol_id =  self.comboBox_rol.currentData()

        #Check de los inputs username, pass y rol
        if not username or rol_id is None:
            msg_boxes.error_msgbox("Campos Obligatorios", "El usuario y el rol no pueden estar vacíos.")
            return False

        if require_password and not password:
            msg_boxes.error_msgbox("Campos Obligatorios", "La contraseña no puede estar vacía.")
            return False

        return True


    def edit(self):
        if not self.verificar_inputs(require_password=False):
            return

        # 1. Capturamos los datos de los componentes de PyQt5
        username = self.input_nameUser.text().strip().upper()
        password = self.input_pass.text().strip()
        nombres = self.input_nombre.text().strip()
        apellidos = self.input_apellido.text().strip()
        
        estado = self.checkBox_activo.isChecked()
        f_inicio = self.dateEdit.date().toPyDate() or date.today()
        f_fin = self.dateEdit_2.date().toPyDate() 

        rol_id =  self.comboBox_rol.currentData()

        try:
            # 2. VALIDACIÓN: Buscamos si el username ya existe usando nuestra nueva función
            usuario_existente = buscar_por_username(username)
            if usuario_existente and usuario_existente['usuario_id'] != self.usuario_id:
                msg_boxes.error_msgbox("Validación", f"El nombre de usuario '{username}' ya está en uso por otro usuario.")
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
                'fecha_fin' : f_fin
            }

            if update(self.usuario_id, data):
                msg_boxes.correct_msgbox("Éxito", f"El usuario '{username}' ha sido actualizado correctamente.")
                self.accept()
            else:
                msg_boxes.error_msgbox("Error", "No se pudo actualizar el usuario en la base de datos.")

        except Exception as e:
            msg_boxes.error_msgbox("Error de Base de Datos", f"Ocurrió un error inesperado.\nDetalle: {e}")


    def limpiar_formulario(self):
        """Limpia todos los campos de la interfaz para un nuevo registro"""
        for campo in (self.input_nameUser, self.input_pass, self.input_nombre, self.input_apellido):
            campo.clear()
        self.checkBox_activo.setChecked(True)
        self.comboBox_rol.setCurrentIndex(0)


