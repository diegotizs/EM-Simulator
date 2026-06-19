"""Espira y solenoide."""
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from elements.base_element import BaseElement
from utils.constants import MU_0

class Coil(BaseElement):
    def __init__(self, position: np.ndarray, orientation: np.ndarray = np.array([1.0, 0.0, 0.0, 0.0])):
        super().__init__(position, orientation)
        self.name = "Espira Circular"
        self.radius = 0.1      # en metros
        self.current = 1.0     # en Amperios
        self.n_turns = 1       # número de vueltas
        self.length = 0.1      # para solenoides

    def get_B_contribution(self, points: np.ndarray) -> np.ndarray:
        """
        Cálculo numérico de Biot-Savart para puntos fuera del eje.
        dB = (mu_0 * I / 4π) * (dl × r̂) / |r|²
        """
        N_segments = 36
        theta = np.linspace(0, 2 * np.pi, N_segments, endpoint=False)
        
        # Geometría base de la espira en el plano XY
        coil_x = self.radius * np.cos(theta)
        coil_y = self.radius * np.sin(theta)
        coil_z = np.zeros_like(theta)
        coil_points = np.column_stack((coil_x, coil_y, coil_z)) + self.position
        
        # Vectores diferenciales de longitud (dl)
        d_theta = 2 * np.pi / N_segments
        dl_x = -self.radius * np.sin(theta) * d_theta
        dl_y =  self.radius * np.cos(theta) * d_theta
        dl_z = np.zeros_like(theta)
        dl = np.column_stack((dl_x, dl_y, dl_z))
        
        B_total = np.zeros_like(points, dtype=np.float64)
        I_total = self.current * self.n_turns # Aproximación para N vueltas apretadas
        factor = (MU_0 * I_total) / (4 * np.pi)
        
        # Integración discreta sumando las contribuciones de los 36 segmentos
        for i in range(N_segments):
            r_vec = points - coil_points[i]
            r_mag = np.linalg.norm(r_vec, axis=1, keepdims=True)
            r_mag = np.where(r_mag == 0, 1e-9, r_mag)
            
            r_hat = r_vec / r_mag
            cross_prod = np.cross(dl[i], r_hat)
            
            dB = factor * cross_prod / (r_mag**2)
            B_total += dB
            
        return B_total

    def get_E_contribution(self, points: np.ndarray) -> np.ndarray:
        return np.zeros_like(points) #

    def get_properties_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Espira: I={self.current}A, r={self.radius}m"))
        widget.setLayout(layout)
        return widget

    def to_dict(self) -> dict:
        return {
            "type": "Coil", 
            "position": self.position.tolist(), 
            "radius": self.radius,
            "current": self.current,
            "n_turns": self.n_turns
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'BaseElement':
        coil = cls(np.array(data["position"]))
        coil.radius = data.get("radius", 0.1)
        coil.current = data.get("current", 1.0)
        coil.n_turns = data.get("n_turns", 1)
        return coil