from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QHBoxLayout, QPushButton, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt, QSize

from models.rol_model import get_all_roles 
from msgboxes import msg_boxes 


class RolPage:
    def __init__(self, ventana_principal):
        # Usaremos self.mainWindow de forma consistente en toda la clase
        self.mainWindow = ventana_principal

        self.main_controller = ventana_principal

        # Configuramos la estructura de la tabla (columnas y encabezados) al iniciar
        self.table_config()

        # Conectamos el botón de la ventana principal al método
        self.mainWindow.btn_addRol.clicked.connect(self.abrir_newRol_ventana)
        
    def abrir_newRol_ventana(self):
        # El import local evita importaciones circulares
        from .newRol_controller import newRol
        
        ventana = newRol(parent=self.mainWindow) 
        ventana.exec_()
        self.cargar_tabla_roles()

    def obtener_rol_id_seleccionado(self):
        """Devuelve el ID del usuario de la fila actualmente seleccionada en la tabla"""
        fila = self.mainWindow.tableROL.currentRow()
        if fila < 0:
            return None
        item = self.mainWindow.tableROL.item(fila, 0)
        return item.data(Qt.UserRole) if item else None

    def abrir_editRol_ventana(self, rol_id):
        """Abre la ventana de edición pasando directamente el ID capturado desde el botón"""
        from .editRol_controller import editRol
        
        ventana = editRol(parent=self.mainWindow, rol_id=rol_id)
        ventana.exec_()
        self.cargar_tabla_roles()  # Recarga de forma segura

        # 2. ¡CRUCIAL! Recargas también la tabla de la página de Usuarios 
        # para que vuelva a leer los nombres de los roles desde la BD
        self.mainWindow.pagina_usuario.cargar_tabla_usuarios()
    
    def abrir_permiso_ventana(self, rol_id):
        """Abre la ventana de edición pasando directamente el ID capturado desde el botón"""
        from .permisos_controller import Permisos
        
        ventana = Permisos(parent=self.mainWindow, rol_id=rol_id)
        ventana.exec_()
        if hasattr(self.mainWindow, 'configurar_accesos_segun_permisos'):
            self.mainWindow.configurar_accesos_segun_permisos()
            
        self.cargar_tabla_roles()  # Recarga de forma segura
    
    def table_config(self):
        """Configura los encabezados y comportamiento de la tabla"""
        column_header = ("Nombre", "Descripción", "Permisos", "Operaciones")
        tabla = self.mainWindow.tableROL

        tabla.setColumnCount(len(column_header))
        tabla.setHorizontalHeaderLabels(column_header)

        # Habilitar ordenación
        tabla.setSortingEnabled(True)
        
        # Ajustes de tamaño visual uniforme
        tabla.setIconSize(QSize(18, 18))
        tabla.verticalHeader().setDefaultSectionSize(35)  # Altura perfecta para albergar botones cómodamente

        header = tabla.horizontalHeader()
        
        for col in (2, 3):
            item = tabla.horizontalHeaderItem(col)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)

        header.setStretchLastSection(True)
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def cargar_tabla_roles(self):
        """Trae los usuarios de la base de datos y llena la QTableWidget directamente"""
        tabla = self.mainWindow.tableROL
        
        # Desactivamos el ordenamiento temporalmente mientras cargamos filas para evitar bugs visuales
        tabla.setSortingEnabled(False)
        
        try:
            lista_roles = get_all_roles() 
            tabla.setRowCount(0)
            
            if not lista_roles:
                msg_boxes.error_msgbox("Aviso", "No se encontraron roles registrados.")
                return 

            tabla.setRowCount(len(lista_roles))
            
            for row_index, rol in enumerate(lista_roles):
                rol_id = rol.get('rol_id')
                nombre = rol.get('nombre') 
                descripcion = rol.get('descripcion') or ''

                # Columna 0: Nombre del rol
                item_nombre = QTableWidgetItem(nombre)
                item_nombre.setData(Qt.UserRole, rol_id)  # Guardamos el ID oculto
                tabla.setItem(row_index, 0, item_nombre)

                # Columna 1: Descripcion del rol
                tabla.setItem(row_index, 1, QTableWidgetItem(str(descripcion)))

                # Columna 2: Permisos 
                tabla.setCellWidget(row_index, 2, self.btn_permiso(rol_id))

                # Columna 3: Operaciones (Pasamos el rol_id a los botones)
                tabla.setCellWidget(row_index, 3, self.btn_operaciones(rol_id))
                
        except Exception as e:
            msg_boxes.error_msgbox("Error", f"No se pudo cargar la lista de roles: {e}")
        finally:
            # Reactivamos el ordenamiento al finalizar la carga
            tabla.setSortingEnabled(True)

    def btn_operaciones(self, rol_id) -> QWidget:
        """Devuelve un QWidget con botones de operaciones mapeados al ID del usuario."""
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        # Botón Editar
        btn_editar = QPushButton()
        btn_editar.setIcon(QIcon(":/white_icons/iconos/edit.svg"))
        btn_editar.setToolTip("Editar rol")
        
        # Solución al bug: Conectamos usando una función lambda con el usuario_id explícito
        btn_editar.clicked.connect(lambda: self.abrir_editRol_ventana(rol_id))
        
        btn_editar.setFixedSize(28, 28)   
        btn_editar.setIconSize(QSize(16, 16))
        btn_editar.setStyleSheet("""
            QPushButton { background-color: #4CAF50; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        # Botón Eliminar
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(QIcon(":/white_icons/iconos/delete.svg"))
        btn_eliminar.setToolTip("Eliminar rol ")
        btn_eliminar.clicked.connect(lambda: self.delete_rol(rol_id))
        
        btn_eliminar.setFixedSize(28, 28)
        btn_eliminar.setIconSize(QSize(16, 16))
        btn_eliminar.setStyleSheet("""
            QPushButton { background-color: #f44336; border-radius: 4px; }
            QPushButton:hover { background-color: #da190b; }
        """)

        layout.addWidget(btn_editar)
        layout.addWidget(btn_eliminar)
        contenedor.setLayout(layout)
        return contenedor

    def btn_permiso(self, rol_id) -> QWidget:
            """Devuelve un QWidget con el botón de permisos mapeado al ID del usuario."""
            contenedor = QWidget()
            layout = QHBoxLayout(contenedor)
            layout.setContentsMargins(5, 2, 5, 2)
            layout.setAlignment(Qt.AlignCenter)

            btn_permiso = QPushButton()
            btn_permiso.setIcon(QIcon(":/white_icons/iconos/config.svg"))
            btn_permiso.setToolTip("Configurar Permisos")
            
            # Mapeado al ID correspondiente
            btn_permiso.clicked.connect(lambda: self.abrir_permiso_ventana(rol_id))
            
            btn_permiso.setFixedSize(28, 28)   
            btn_permiso.setIconSize(QSize(16, 16))
            btn_permiso.setStyleSheet("""
                QPushButton { background-color: #757575; border-radius: 4px; }
                QPushButton:hover { background-color: #616161; }
            """)

            layout.addWidget(btn_permiso)
            contenedor.setLayout(layout)
            return contenedor
