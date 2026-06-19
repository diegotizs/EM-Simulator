"""Punto de entrada. Inicializa QApplication y MainWindow."""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EM Simulator")
        self.resize(1024, 768)
        # Aquí se ensamblarán los widgets de gui/ en las siguientes fases

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())