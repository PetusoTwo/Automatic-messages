import sys
import pywhatkit as kit
import time
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIntValidator
from help import Ui_MainWindow

def enviar_mensajes(numeros, mensaje, wait_time):
    # Recorre la lista de números y envía el mensaje a cada uno
    for numero in numeros:
        try:
            # Envía el mensaje
            kit.sendwhatmsg_instantly(numero, mensaje, wait_time=5, tab_close=True, close_time=2)
            print(f"Mensaje enviado a {numero}")
            # Tiempo para que el programa espere antes de enviar otro mensaje, para evitar errores
            time.sleep(wait_time)
        except Exception as e:
            print(f"No se pudo enviar el mensaje a {numero}: {e}")

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        # Cargamos el diseño hecho en Qt Designer
        uic.loadUi("./design.ui", self)
        
        # Configuraciones de ventana para quitar iconos de arriba (x - maximizar - minimizar)
        self.setWindowOpacity(1)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Variables para el movimiento de la ventana
        self.click_position = None
        
        # Conecta el botón 'send' con la función para enviar mensajes y también con la función para limpiar los datos
        self.send.clicked.connect(self.enviar)
        self.send.clicked.connect(self.clearData)
        self.help.clicked.connect(self.abrirAyuda)
        # Conecta el botón 'close' para cerrar la ventana
        self.btn_close.clicked.connect(lambda: self.close())

    def abrirAyuda(self):
        self.ventana_ayuda = QtWidgets.QMainWindow()
        uic.loadUi("./help.ui", self.ventana_ayuda)
        
        # Botón de cerrar
        self.ventana_ayuda.btn_close.clicked.connect(lambda: self.ventana_ayuda.close())
        
        # Configuraciones de ventana para quitar iconos de arriba (x - maximizar - minimizar)
        self.ventana_ayuda.setWindowOpacity(1)
        self.ventana_ayuda.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.ventana_ayuda.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.ventana_ayuda.show()
    
    def enviar(self):
        # Obtiene los datos de los QLineEdit
        mensaje = self.mensaje.text()
        wait_time_str = self.time.text()
        numeros_str = self.telefonos.text()
        
        # Validación de que el campo 'mensaje' no esté vacío
        if not mensaje.strip():
            self.mostrarError("Error", "Campo vacio: Ingrese el mensaje a mandar.")
            return
        
        # Validación de que el campo 'time' contenga solo números
        try:
            wait_time = int(wait_time_str)
        except ValueError:
            self.mostrarError("Error", "El tiempo de espera debe ser un número entero (Segundos).")
            return
        
        numeros = self.telefonos.text().split(",")
        # Llama a la función para enviar los mensajes
        enviar_mensajes(numeros, mensaje, wait_time)

        # Muestra un mensaje de éxito
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(f"Mensaje enviado correctamente a {numeros} :D")
        msg_box.setWindowTitle("Éxito")
        msg_box.exec()

    def clearData(self):
        # Función para limpiar los datos de los QLineEdit
        self.telefonos.setText("")
        self.mensaje.setText("")
        self.time.setText("")
    
    # Función para mostrar un mensaje de error y solo llamarla en la función 'enviar' y pasar solo los parametros
    def mostrarError(self, title, message):
        # Función para mostrar un mensaje de error
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec()


#Funciones para que la ventana se pueda mover#
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_position = event.globalPosition().toPoint()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.click_position is not None:
            self.move(self.pos() + event.globalPosition().toPoint() - self.click_position)
            self.click_position = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.click_position = None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
