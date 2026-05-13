from PyQt5.QtWidgets import QMessageBox


class MsgBox(QMessageBox):
    def __init__(self, titulo, texto, icono_qt):
        super().__init__()
        self.setWindowTitle(titulo)
        self.setText(texto)

        self.setIcon(icono_qt)   


    def set_yes_no_buttons(self):
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)


def correct_msgbox(titulo, texto):
    msg_box = MsgBox(titulo, texto, QMessageBox.Icon.Information)
    msg_box.exec_()

def error_msgbox(titulo, texto):
    msg_box = MsgBox(titulo, texto, QMessageBox.Icon.Critical)
    msg_box.exec_()

def warning_msgbox(titulo, texto):
    msg_box = MsgBox(titulo, texto, QMessageBox.Icon.Warning)
    msg_box.set_yes_no_buttons()
    resp =  msg_box.exec_()
    return resp

