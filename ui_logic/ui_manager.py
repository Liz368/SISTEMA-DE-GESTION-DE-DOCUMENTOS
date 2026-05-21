from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject

class VentanaUILogic(QObject):
    def __init__(self, ventana):
        super().__init__()
       
        self.v = ventana # Guardamos la referencia a la ventana principal

       # 1. Creamos un diccionario: {Botón: Índice de la página}
        # Agrupamos tanto el botón de texto como el de icono al mismo índice
        self.mapeo_paginas = {
            self.v.btn_inicio: 0,
            self.v.btn_inicio_icon: 0,
            self.v.btn_doc: 1,
            self.v.btn_doc_icon: 1,
            self.v.btn_user: 3,
            self.v.btn_user_icon: 3,
            self.v.btn_rol: 4,
            self.v.btn_rol_icon: 4,
            self.v.btn_bitacora: 5,
            self.v.btn_bit_icon: 5,
            self.v.btn_catg: 6,
            self.v.btn_catg_icon: 6,
            
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

    
   

   

  
        
  
   