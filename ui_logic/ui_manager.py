from PyQt5.QtWidgets import QMenu, QAction, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QObject, Qt

# ==============================================================================
# TARJETA DE NOTIFICACIÓN INDIVIDUAL
# ==============================================================================
class TarjetaNotificacion(QWidget):
    def __init__(self, mensaje, hora):
        super().__init__()
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(5, 5, 5, 5)
        layout_principal.setSpacing(10)
        
        self.foto_usuario = QLabel()
        self.foto_usuario.setFixedSize(40, 40)
        self.foto_usuario.setStyleSheet("""
            background-color: #e2e8f0;   
            border-radius: 20px;         
            border: 1px solid #cbd5e1;
        """)
        layout_principal.addWidget(self.foto_usuario)
        
        layout_textos = QVBoxLayout()
        layout_textos.setSpacing(2)
        
        label_mensaje = QLabel(mensaje)
        label_mensaje.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: bold; background: transparent;")
        label_mensaje.setWordWrap(True)  
        
        label_hora = QLabel(hora)
        label_hora.setStyleSheet("color: #cbd5e1; font-size: 11px; background: transparent;")
        
        layout_textos.addWidget(label_mensaje)
        layout_textos.addWidget(label_hora)
        
        layout_principal.addLayout(layout_textos)

# ==============================================================================
# PANEL CONTENEDOR DE NOTIFICACIONES
# ==============================================================================
class PanelNotificaciones(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedWidth(320)
        
        layout_dialogo = QVBoxLayout(self)
        layout_dialogo.setContentsMargins(0, 0, 0, 0)
        
        self.contenedor_visual = QFrame()
        self.contenedor_visual.setObjectName("ContenedorAzul")
        self.contenedor_visual.setStyleSheet("""
            QFrame#ContenedorAzul {
                background-color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 15px;
            }
        """)
        
        self.layout_panel = QVBoxLayout(self.contenedor_visual)
        self.layout_panel.setContentsMargins(15, 15, 15, 15)
        layout_dialogo.addWidget(self.contenedor_visual)
        
        # Ejemplos iniciales
        self.agregar_notificacion("Carlos subió un documento PDF", "Hace 5 min")
        self.agregar_notificacion("María subió el informe final", "14:30 PM")

    def agregar_notificacion(self, mensaje, hora):
        tarjeta = TarjetaNotificacion(mensaje, hora)
        self.layout_panel.addWidget(tarjeta)
        
        linea = QWidget()
        linea.setFixedHeight(1)
        linea.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        self.layout_panel.addWidget(linea)

    

class VentanaUILogic(QObject):
    def __init__(self, ventana):
        super().__init__()
       
        self.v = ventana # Guardamos la referencia a la ventana principal

       # 1. Creamos un diccionario: {Botón: Índice de la página}
        # Agrupamos tanto el botón de texto como el de icono al mismo índice
        self.mapeo_paginas = {
            self.v.btn_inicio: 0,
            self.v.btn_inicio_icon: 0,
            self.v.btn_resol: 1,
            self.v.btn_resol_icon: 1,
            self.v.btn_regla: 2,
            self.v.btn_regla_icon: 2,
            self.v.btn_user: 3,
            self.v.btn_user_icon: 3,
            self.v.btn_rol: 4,
            self.v.btn_rol_icon: 4,
            self.v.btn_bitacora: 5,
            self.v.btn_bit_icon: 5,
            self.v.btn_tp_resol: 6,
            self.v.btn_tp_resol_icon: 6,
            self.v.btn_tp_regla: 7,
            self.v.btn_tp_regla_icon: 7,
            self.v.btn_reports: 8,
            self.v.btn_reports_icon: 8
            
        }

        # 2. Conectamos todos los botones a la MISMA función
        for boton in self.mapeo_paginas.keys():
            boton.clicked.connect(self.cambiar_pagina)

        

    def cambiar_pagina(self):
        # 'self.sender()' nos dice exactamente qué botón fue presionado
        boton_presionado = self.sender()
        
        # Obtenemos el índice correspondiente del diccionario
        indice = self.mapeo_paginas.get(boton_presionado)
    
        if indice is not None:
            self.v.stackedWidget_2.setCurrentIndex(indice)
            print(f"Cambiando a página: {indice}") # Opcional para depurar
        

    def aplicar_configuracion_inicial(self):
        """Este método centraliza los estados iniciales de la UI"""
        self.v.stackedWidget_2.setCurrentIndex(0)
        self.v.MenuIconsContainer.hide()
        self.v.btn_menu.setChecked(True)

    
    def configurar_menu_usuario(self, boton):
        boton.setMenu(None)
        # 1. Forzamos a quitar la flecha mediante código en el botón
        boton.setStyleSheet("QPushButton::menu-indicator { width: 0px; display: none; image: none; }")

        menu = QMenu(self.v)

        # --- AQUÍ ESTÁ EL TRUCO PARA ELIMINAR LAS ESQUINAS CUADRADAS ---
        menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        menu.setAttribute(Qt.WA_TranslucentBackground)

        # 2. PERSONALIZACIÓN DEL MENÚ (Colores y Esquinas Redondeadas)
        menu.setStyleSheet("""
            QMenu {
                background-color: #59788E;       /* Color de fondo del menú (Oscuro) */
                color: #ffffff;                  /* Color del texto (Blanco) */
                border: 1px solid #59788E;      /* Borde sutil alrededor del menú */
                border-radius: 12px;              /* ¡AQUÍ SE REDONDEAN LAS ESQUINAS! */
                padding: 3px;                    /* Espacio interno para que no se vea apretado */
                margin: 5px;
            }
            
            QMenu::item {
                background-color: transparent;
                color: white;
                padding: 8px 25px;
                border-radius: 6px;
            }
            
            QMenu::item:selected {
                background-color: #c8c8c8;       /* Color de fondo cuando pasas el mouse (Azul) */   
            }
            
            QMenu::separator {
                height: 1px;
                background-color: rgba(255, 255, 255, 0.6);       /* Color de la línea divisoria */
                margin: 6px 10px;                /* Separación de la línea con los bordes */
            }
        """)
        
        accion_perfil = QAction("Mi Perfil", self)
        accion_config = QAction("Configuración", self)
        accion_salir = QAction("Cerrar Sesión", self)
        
        # Conexiones a funciones
        accion_perfil.triggered.connect(self.abrir_perfil)
        accion_config.triggered.connect(self.abrir_configuracion)
        accion_salir.triggered.connect(self.cerrar_sesion)
        
        menu.addAction(accion_perfil)
        menu.addSeparator() # Agrega el separador directo si prefieres
        menu.addAction(accion_config)
        menu.addSeparator()
        menu.addAction(accion_salir)
        
        # Vincular menú al botón
        boton.clicked.connect(lambda: menu.exec_(boton.mapToGlobal(boton.rect().bottomLeft())))

    # --- DEFINE AQUÍ LO QUE HACE CADA OPCIÓN AL HACER CLIC ---
    def abrir_perfil(self):
        print("Abriendo el perfil del usuario...")

    def abrir_configuracion(self):
        print("Abriendo ajustes...")

    def cerrar_sesion(self):
        print("Cerrando sesión...")

    def configurar_notificaciones(self, boton_notificaciones):
        """Inicializa el panel flotante y lo vincula al botón de la barra superior"""
        # 1. Creamos el panel usando 'self.v' como ventana padre
        self.panel_notis = PanelNotificaciones(self.v)
        
        # 2. Conectamos el clic del botón a la lógica de posicionamiento animado/flotante
        boton_notificaciones.clicked.connect(lambda: self.mostrar_panel_notificaciones(boton_notificaciones))

    def mostrar_panel_notificaciones(self, boton):
        """Calcula la posición exacta debajo del botón y muestra el panel"""
        posicion_global = boton.mapToGlobal(boton.rect().bottomLeft())
        x = posicion_global.x() - (self.panel_notis.width() - boton.width())
        y = posicion_global.y() + 8
        
        self.panel_notis.move(x, y)
        self.panel_notis.show()


   

   

  
        
  
   