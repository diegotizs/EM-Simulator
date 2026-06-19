"""Clase abstracta base para los elementos físicos de la escena."""
from abc import ABC, abstractmethod
import numpy as np
import uuid
from PyQt6.QtWidgets import QWidget

class BaseElement(ABC):
    def __init__(self, position: np.ndarray, orientation: np.ndarray):
        self.position: np.ndarray = position      # [x, y, z] en metros
        self.orientation: np.ndarray = orientation  # cuaternión [w, x, y, z]
        self.id: str = str(uuid.uuid4())          # UUID único, asignado al crear
        self.name: str = "Elemento Base"          # Nombre legible
        self.is_selected: bool = False
        self.is_active: bool = True               # Si False, no contribuye al campo

    @abstractmethod
    def get_B_contribution(self, points: np.ndarray) -> np.ndarray:
        """
        Calcula la contribución de este elemento al campo B en los puntos dados.
        - points: shape (N, 3) — coordenadas donde se evalúa el campo
        - returns: shape (N, 3) — vector B en cada punto, en Teslas
        """
        pass

    @abstractmethod
    def get_E_contribution(self, points: np.ndarray) -> np.ndarray:
        """
        Calcula la contribución de este elemento al campo E en los puntos dados.
        - points: shape (N, 3) — coordenadas donde se evalúa el campo
        - returns: shape (N, 3) — vector E en cada punto, en V/m
        """
        pass

    @abstractmethod
    def get_properties_widget(self) -> QWidget:
        """
        Retorna el widget Qt con los controles de propiedades de este elemento.
        Este widget se muestra en el panel de control cuando el elemento está seleccionado.
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serializa el elemento a un dict para guardarlo en JSON."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'BaseElement':
        """Reconstruye el elemento desde un dict cargado de JSON."""
        pass