"""Imán permanente (dipolo magnético)."""
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from elements.base_element import BaseElement
from utils.constants import MU_0

class Magnet(BaseElement):
    def __init__(self, position: np.ndarray, orientation: np.ndarray = np.array([1.0, 0.0, 0.0, 0.0])):
        super().__init__(position, orientation)
        self.name = "Imán Permanente"
        self.dipole_moment = 1.0  # Magnitud en A·m²
        # Dirección local. Asumimos el eje Z por ahora para la Fase 1
        self.direction = np.array([0.0, 0.0, 1.0])

    def get_B_contribution(self, points: np.ndarray) -> np.ndarray:
        # points shape: (N, 3)
        r_vec = points - self.position
        r_mag = np.linalg.norm(r_vec, axis=1, keepdims=True)
        
        # Evitar singularidad matemática en el origen exacto del dipolo
        r_mag = np.where(r_mag == 0, 1e-9, r_mag)
        r_hat = r_vec / r_mag
        
        # Vector del momento dipolar (1, 3)
        m_vec = self.dipole_moment * self.direction
        
        # Producto punto escalar (m · r_hat)
        m_dot_r = np.sum(m_vec * r_hat, axis=1, keepdims=True)
        
        # Aplicación directa de la fórmula del dipolo
        term1 = 3 * m_dot_r * r_hat
        term2 = m_vec
        
        B = (MU_0 / (4 * np.pi)) * (term1 - term2) / (r_mag**3)
        return B

    def get_E_contribution(self, points: np.ndarray) -> np.ndarray:
        return np.zeros_like(points) # Los imanes no emiten campo E estacionario

    def get_properties_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Imán: {self.dipole_moment} A·m²"))
        widget.setLayout(layout)
        return widget

    def to_dict(self) -> dict:
        return {"type": "Magnet", "position": self.position.tolist(), "dipole_moment": self.dipole_moment}

    @classmethod
    def from_dict(cls, data: dict) -> 'BaseElement':
        mag = cls(np.array(data["position"]))
        mag.dipole_moment = data.get("dipole_moment", 1.0)
        return mag