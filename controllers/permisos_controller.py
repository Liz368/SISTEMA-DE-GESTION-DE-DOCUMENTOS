from PyQt5.QtWidgets import QDialog, QMessageBox
from ui_files.permisos_ui import Ui_permisosDialog
from models.permisos_model import get_all_permisos, get_permisos_por_rol, asignar_permiso_a_rol, revocar_permiso_de_rol

class Permisos(QDialog, Ui_permisosDialog): # O QMainWindow, dependiendo de qué componente usaste en Designer
    def __init__(self, rol_id, parent=None):
        super().__init__(parent)
        
        self.setupUi(self)  # <-- Descomenta esto para cargar tu diseño de Qt Designer
        
        self.rol_id = rol_id  # Guardamos el ID del rol que estamos configurando
        
        # =====================================================================
        # DICCIONARIO DE MAPEO (Crucial para tu diseño)
        # =====================================================================
        # Vincula el 'nombre' exacto del permiso en tu base de datos
        # con el nombre que le diste al objeto QCheckBox en Qt Designer.
        self.mapa_permisos = {
            'menu_home': self.chk_ver_home,       # Coincide con tu INSERT de 'menu_home'
            'menu_documentos': self.chk_ver_doc, # Coincide con tu INSERT de 'menu_documentos'
            'menu_usuarios': self.chk_ver_user,   # (Necesita estar insertado en la BD)
            'menu_roles': self.chk_ver_rol, # Solo para probar el botón de agregar
            # ... etc ...
        }

        # Conexión de eventos
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_guardar.setShortcut("Return")
        
        # 1. Limpiamos y cargamos los estados actuales en la pantalla
        self.cargar_permisos_en_interfaz()
        
        # 2. Conectamos los botones de acción
        self.btn_guardar.clicked.connect(self.guardar_cambios)

    def cargar_permisos_en_interfaz(self):
        """Busca qué permisos tiene el rol en la BD y marca los checkboxes correspondientes"""
        try:
            # Desmarcamos todos los checkboxes por seguridad antes de empezar
            for checkbox in self.mapa_permisos.values():
                checkbox.setChecked(False)
            
            # Traemos la lista de permisos que este rol específico ya tiene asignados
            # Devuelve una lista de diccionarios gracias a RealDictCursor
            permisos_actuales = get_permisos_por_rol(self.rol_id)
            
            # Recorremos los resultados y activamos los que coincidan en nuestro mapa
            for perm in permisos_actuales:
                nombre_permiso = perm['nombre']
                if nombre_permiso in self.mapa_permisos:
                    self.mapa_permisos[nombre_permiso].setChecked(True)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los permisos actuales: {e}")

    def guardar_cambios(self):
        """Compara la interfaz con la BD para añadir o remover los permisos de este rol"""
        try:
            # 1. Traemos todos los permisos del sistema para conocer sus IDs oficiales
            todos_los_permisos = get_all_permisos()
            
            # Convertimos la lista a un diccionario para buscar rápido por nombre: {'user_crear': 5}
            diccionario_ids = {p['nombre']: p['permiso_id'] for p in todos_los_permisos}
            
            # 2. Recorremos nuestro mapa checkbox por checkbox
            for nombre_permiso, checkbox in self.mapa_permisos.items():
                permiso_id = diccionario_ids.get(nombre_permiso)
                
                if not permiso_id:
                    print(f"Advertencia: El permiso '{nombre_permiso}' no existe en la tabla de la BD.")
                    continue
                
                # Si el checkbox está marcado en la UI, aseguramos que esté en la BD
                if checkbox.isChecked():
                    asignar_permiso_a_rol(self.rol_id, permiso_id)
                else:
                    # Si está desmarcado, nos aseguramos de revocarlo
                    revocar_permiso_de_rol(self.rol_id, permiso_id)
            
            QMessageBox.information(self, "Éxito", "Permisos del rol actualizados correctamente.")
            self.accept()  # Cierra la ventana indicando que todo salió bien
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar los cambios: {e}")