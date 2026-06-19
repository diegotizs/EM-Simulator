"""Cálculo de campos E y B en la grilla 3D."""
import numpy as np

def make_grid(bounds: tuple, resolution: int) -> np.ndarray:
    """
    Crea una grilla 3D uniforme.
    - bounds: (x_min, x_max, y_min, y_max, z_min, z_max) en metros
    - resolution: número de puntos por eje
    - returns: shape (resolution^3, 3) con las coordenadas de todos los puntos
    """
    x = np.linspace(bounds[0], bounds[1], resolution)
    y = np.linspace(bounds[2], bounds[3], resolution)
    z = np.linspace(bounds[4], bounds[5], resolution)
    
    # meshgrid con indexing='ij' para mantener la consistencia en los ejes espaciales
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Aplanamos a una matriz Nx3 para vectorizar los cálculos en NumPy fácilmente
    grid_points = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    return grid_points

def compute_B_field(elements: list, grid_points: np.ndarray) -> np.ndarray:
    """
    Calcula el campo B total en todos los puntos de la grilla usando superposición.
    Internamente llama a element.get_B_contribution() y suma los resultados.
    """
    B_total = np.zeros_like(grid_points, dtype=np.float64)
    for el in elements:
        if el.is_active:
            B_total += el.get_B_contribution(grid_points)
    return B_total

def compute_E_field(elements: list, grid_points: np.ndarray) -> np.ndarray:
    """
    Igual que compute_B_field pero para el campo eléctrico en V/m.
    """
    E_total = np.zeros_like(grid_points, dtype=np.float64)
    for el in elements:
        if el.is_active:
            E_total += el.get_E_contribution(grid_points)
    return E_total

def compute_cross_product_field(J_field: np.ndarray, B_field: np.ndarray) -> np.ndarray:
    """
    Calcula F = J × B en cada punto de la grilla.
    """
    return np.cross(J_field, B_field)