"""Punto de entrada. Inicializa QApplication y MainWindow."""
import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow
from renderer.scene3d import Scene3D
from elements.magnet import Magnet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EM Simulator - Fase 1")
        self.resize(1024, 768)
        
        # 1. Crear el lienzo 3D y ponerlo en el centro de la ventana
        self.scene_widget = Scene3D()
        self.setCentralWidget(self.scene_widget)
        
        # 2. Crear un imán de prueba y añadirlo a la escena
        test_magnet = Magnet(position=np.array([0.0, 0.0, 0.0]))
        test_magnet.dipole_moment = 0.5  # Lo ajustamos para que se vea bien en la escala
        
        self.scene_widget.elements.append(test_magnet)

    def showEvent(self, event):
        """Se asegura de calcular la física solo después de que OpenGL arrancó."""
        super().showEvent(event)
        self.scene_widget.update_fields()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())