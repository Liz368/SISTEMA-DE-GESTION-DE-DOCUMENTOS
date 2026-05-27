from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QEvent 
from ui_files.editRol_ui import  Ui_DialogEditarRol
from models.rol_model import get_rol_by_id, get_rol_nombre, update
from msgboxes import msg_boxes 

class editRol(QDialog, Ui_DialogEditarRol):
    
    def __init__(self, parent=None, rol_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.rol_id = rol_id

        # Conexión de eventos
        self.btn_guardar.clicked.connect(self.edit)
        self.btn_guardar.setShortcut("Return")
        
        for campo in (self.input_nombre, self.input_des):
            campo.installEventFilter(self)

        if  self.rol_id:
            self.cargar_datos_rol(self.rol_id)


    def cargar_datos_rol(self, rol_id):
        roles = get_rol_by_id(rol_id)
        if roles:
            self.input_nombre.setText(roles['nombre'])
            self.input_des.setPlainText(roles['descripcion'])

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.btn_guardar.click()
            return True
        return super().eventFilter(obj, event)
    
    def verificar_inputs(self):
        nombre = self.input_nombre.text().strip()

        #Check de los inputs username, pass y rol
        if not nombre:
            msg_boxes.error_msgbox("Campos Obligatorio", "El nombre de rol no puede estar vacío.")
            return False
        return True


    def edit(self):
        if not self.verificar_inputs():
            return

        # 1. Capturamos los datos de los componentes de PyQt5
        nombre = self.input_nombre.text().strip()
        descripcion = self.input_des.toPlainText().strip()

        try:
            # 2. VALIDACIÓN: Buscamos si el username ya existe usando nuestra nueva función
            rol_existente = get_rol_nombre(nombre)
            if rol_existente and rol_existente['rol_id'] != self.rol_id:
                msg_boxes.error_msgbox("Validación", f"El nombre de rol '{nombre}' ya está en uso.")
                return

            # 3. ARMAMOS EL DICCIONARIO: En el orden exacto que espera tu función insert()
            data = {
                'nombre': nombre,
                'descripcion': descripcion,
            }

            if update(self.rol_id, data):
                msg_boxes.correct_msgbox("Éxito", f"El rol '{nombre}' ha sido actualizado correctamente.")
                self.accept()
            else:
                msg_boxes.error_msgbox("Error", "No se pudo actualizar el rol en la base de datos.")

        except Exception as e:
            msg_boxes.error_msgbox("Error de Base de Datos", f"Ocurrió un error inesperado.\nDetalle: {e}")



