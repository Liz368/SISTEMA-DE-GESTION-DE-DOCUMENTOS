# controllers/usuario_controller.py
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QHBoxLayout, QPushButton, QWidget, QAbstractItemView
from PyQt5.QtCore import Qt, QSize

from models.usuario_model import get_all 
from msgboxes import msg_boxes 

class UsuarioPage:
    def __init__(self, ventana_principal):
        # Usaremos self.mainWindow de forma consistente en toda la clase
        self.mainWindow = ventana_principal

        # Configuramos la estructura de la tabla (columnas y encabezados) al iniciar
        self.table_config()

        # Conectamos el botón de la ventana principal al método
        self.mainWindow.btn_addUser.clicked.connect(self.abrir_newUser_ventana)
        self.mainWindow.boxEstado.currentIndexChanged.connect(self.aplicar_filtros)
        self.mainWindow.input_busqueda.textChanged.connect(self.aplicar_filtros)
        
        

    def abrir_newUser_ventana(self):
        # El import local evita importaciones circulares
        from .newUser_controller import newUser
        
        ventana = newUser(parent=self.mainWindow) 
        ventana.exec_()
        self.cargar_tabla_usuarios()
    
    def obtener_usuario_id_seleccionado(self):
        """Devuelve el ID del usuario de la fila actualmente seleccionada en la tabla"""
        fila = self.mainWindow.tableUSER.currentRow()
        if fila < 0:
            return None
        item = self.mainWindow.tableUSER.item(fila, 0)
        return item.data(Qt.UserRole) if item else None

    def abrir_editUser_ventana(self, usuario_id):
        """Abre la ventana de edición pasando directamente el ID capturado desde el botón"""
        from .editUser_controller import editUser
        
        ventana = editUser(parent=self.mainWindow, usuario_id=usuario_id)
        ventana.exec_()
        self.cargar_tabla_usuarios()  # Recarga de forma segura

    def table_config(self):
        """Configura los encabezados y comportamiento de la tabla"""
        column_header = ("Nombre Completo", "Estado", "Username", "Rol", "Fecha Inicio", "Operaciones")
        tabla = self.mainWindow.tableUSER

        tabla.setColumnCount(len(column_header))
        tabla.setHorizontalHeaderLabels(column_header)

        # Habilitar ordenación
        tabla.setSortingEnabled(True)
        
        # Ajustes de tamaño visual uniforme
        tabla.setIconSize(QSize(18, 18))
        tabla.verticalHeader().setDefaultSectionSize(35)  # Altura perfecta para albergar botones cómodamente

        header = tabla.horizontalHeader()
        
        # Desactivar ordenación en columnas que contienen widgets/botones (Permisos=3, Operaciones=5)
        # Nota: En PyQt, para desactivar la ordenación por columnas específicas de forma robusta,
        # lo ideal es manejarlo al cargar los datos o deshabilitar visualmente el click, 
        # pero quitar flags del header previene comportamientos raros.
        for col in (3, 5):
            item = tabla.horizontalHeaderItem(col)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)

        header.setStretchLastSection(True)
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def cargar_tabla_usuarios(self):
        """Trae los usuarios de la base de datos y llena la QTableWidget directamente"""
        tabla = self.mainWindow.tableUSER
        
        # Desactivamos el ordenamiento temporalmente mientras cargamos filas para evitar bugs visuales
        tabla.setSortingEnabled(False)
        
        try:
            lista_usuarios = get_all() 
            tabla.setRowCount(0)
            
            if not lista_usuarios:
                msg_boxes.error_msgbox("Aviso", "No se encontraron usuarios registrados.")
                return 

            tabla.setRowCount(len(lista_usuarios))
            
            for row_index, usuario in enumerate(lista_usuarios):
                usuario_id = usuario.get('usuario_id')
                nombre_completo = f"{usuario.get('nombres','')} {usuario.get('apellidos','')}".strip() or usuario.get('username','')
                username_upper = (usuario.get('username') or '').upper()
                rol_id = usuario.get('rol_id')
                rol_nombre = usuario.get('rol_nombre') 
                estado = usuario.get('estado', False)
                fecha_ingreso = str(usuario.get('fecha_inicio', ''))

                # Columna 0: Nombre completo
                item_nombre = QTableWidgetItem(nombre_completo)
                item_nombre.setData(Qt.UserRole, usuario_id)  # Guardamos el ID oculto
                tabla.setItem(row_index, 0, item_nombre)

               # Columna 1: Estado (¡Centrado nativo, protegido contra edición y ordenable!)
                tabla.setItem(row_index, 1, self.icono_estado(estado))

                # Columna 2: Username
                tabla.setItem(row_index, 2, QTableWidgetItem(username_upper))

                # Columna 4: Rol
                tabla.setItem(row_index, 3, QTableWidgetItem(rol_nombre))

                # Columna 4: Fecha de Ingreso del usuario
                tabla.setItem(row_index, 4, QTableWidgetItem(fecha_ingreso))

                # Columna 5: Operaciones (Pasamos el usuario_id a los botones)
                tabla.setCellWidget(row_index, 5, self.btn_operaciones(usuario_id))
                
        except Exception as e:
            msg_boxes.error_msgbox("Error", f"No se pudo cargar la lista de usuarios: {e}")
        finally:
            # Reactivamos el ordenamiento al finalizar la carga
            tabla.setSortingEnabled(True)
            self.aplicar_filtros()


    def icono_estado(self, estado: bool) -> QTableWidgetItem:
        """
        Crea y configura un QTableWidgetItem nativo con el ícono centrado,
        guardando un valor numérico ordenable y bloqueando la edición.
        """
        item = QTableWidgetItem()
        
        # 1. Guardamos el 1 o 0 de forma nativa para ordenamiento y filtros
        item.setData(Qt.UserRole, 1 if estado else 0)

        # 2. Asignamos el ícono correspondiente desde tus recursos
        ruta_icono = ":/white_icons/iconos/correct-98.svg" if estado else ":/white_icons/iconos/error-35.svg"
        item.setIcon(QIcon(ruta_icono))

        # 3. Estética: Texto transparente y centrado nativo
        item.setForeground(Qt.transparent)
        item.setTextAlignment(Qt.AlignCenter)

        # 4. SEGURIDAD: Solo activado y seleccionable (NO editable)
        # Esto evita que el usuario pueda abrir un cuadro de texto al dar doble clic
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        return item
        
    def btn_operaciones(self, usuario_id) -> QWidget:
        """Devuelve un QWidget con botones de operaciones mapeados al ID del usuario."""
        contenedor = QWidget()
        layout = QHBoxLayout(contenedor)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        # Botón Editar
        btn_editar = QPushButton()
        btn_editar.setIcon(QIcon(":/white_icons/iconos/edit.svg"))
        btn_editar.setToolTip("Editar usuario")
        
        # Solución al bug: Conectamos usando una función lambda con el usuario_id explícito
        btn_editar.clicked.connect(lambda: self.abrir_editUser_ventana(usuario_id))
        
        btn_editar.setFixedSize(28, 28)   
        btn_editar.setIconSize(QSize(16, 16))
        btn_editar.setStyleSheet("""
            QPushButton { background-color: #4CAF50; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
        """)

        # Botón Eliminar
        btn_eliminar = QPushButton()
        btn_eliminar.setIcon(QIcon(":/white_icons/iconos/delete.svg"))
        btn_eliminar.setToolTip("Eliminar usuario")
        btn_eliminar.clicked.connect(lambda: self.delete_user(usuario_id))
        
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
    
   
    def delete_user(self, usuario_id):
        # Aquí puedes implementar tu lógica de borrado usando directamente el usuario_id
        pass

    def vista_user(self):
        pass

    def aplicar_filtros(self):
        """
        Aplica ambos filtros: estado + búsqueda.
        """
        texto = self.mainWindow.input_busqueda.text().strip().lower()
        index_estado = self.mainWindow.boxEstado.currentIndex()
        tabla = self.mainWindow.tableUSER

        for fila in range(tabla.rowCount()):
            cumple_estado = self.filtrar_por_estado(fila, index_estado)
            cumple_busqueda = self.filtrar_por_busqueda(fila, texto)

            # Mostrar solo si cumple ambos
            mostrar_fila = cumple_estado and cumple_busqueda
            tabla.setRowHidden(fila, not mostrar_fila)


    def filtrar_por_estado(self, fila, index_estado):
        """
        Devuelve True si la fila cumple con el filtro de estado.
        """
        item_estado = self.mainWindow.tableUSER.item(fila, 1)
        if not item_estado:
            return True  # Si no hay estado, no ocultamos

        valor_estado = item_estado.data(Qt.UserRole)  # 1 activo, 0 inactivo

        if index_estado == 1 and valor_estado != 1:   # Activos
            return False
        elif index_estado == 2 and valor_estado != 0: # Inactivos
            return False
        return True

    def filtrar_por_busqueda(self, fila, texto):
        """
        Devuelve True si la fila cumple con el filtro de búsqueda.
        Ignora columnas con botones (3 y 5).
        """
        if not texto:
            return True  # Si no hay texto, no filtramos

        for col in range(self.mainWindow.tableUSER.columnCount()):
            if col == 5:  # Ignorar columnas con botones
                continue
            item = self.mainWindow.tableUSER.item(fila, col)
            if item and texto in item.text().lower():
                return True
        return False