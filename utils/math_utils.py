"""Funciones matemáticas vectoriales auxiliares."""
import numpy as np
from scipy.interpolate import RegularGridInterpolator

def normalize(v: np.ndarray) -> np.ndarray:
    """Normaliza un vector. Retorna vector cero si la magnitud es cero."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return np.zeros_like(v)
    return v / norm

def cross3(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Producto cruzado para arrays de shape (N, 3). Wrappea np.cross."""
    return np.cross(a, b)

def curl(field: np.ndarray, dx: float) -> np.ndarray:
    """Calcula el rotacional de un campo vectorial en una grilla regular."""
    # Gradientes a lo largo de cada eje
    dy_dz, dy_dy, dy_dx = np.gradient(field[..., 1], dx, edge_order=2)
    dz_dz, dz_dy, dz_dx = np.gradient(field[..., 2], dx, edge_order=2)
    dx_dz, dx_dy, dx_dx = np.gradient(field[..., 0], dx, edge_order=2)
    
    rot_x = dz_dy - dy_dz
    rot_y = dx_dz - dz_dx
    rot_z = dy_dx - dx_dy
    
    return np.stack((rot_x, rot_y, rot_z), axis=-1)

def divergence(field: np.ndarray, dx: float) -> np.ndarray:
    """Calcula la divergencia de un campo vectorial en una grilla regular."""
    dx_dx = np.gradient(field[..., 0], dx, axis=0, edge_order=2)
    dy_dy = np.gradient(field[..., 1], dx, axis=1, edge_order=2)
    dz_dz = np.gradient(field[..., 2], dx, axis=2, edge_order=2)
    return dx_dx + dy_dy + dz_dz

def interpolate_field(field: np.ndarray, grid_bounds: tuple, point: np.ndarray) -> np.ndarray:
    """
    Interpola el campo vectorial en un punto arbitrario usando interpolación trilineal.
    Wrappea scipy.interpolate.RegularGridInterpolator.
    """
    # Esta es una implementación básica; en producción es mejor crear el interpolador 
    # una sola vez y llamarlo múltiples veces por rendimiento.
    nx, ny, nz = field.shape[:3]
    x = np.linspace(grid_bounds[0], grid_bounds[1], nx)
    y = np.linspace(grid_bounds[2], grid_bounds[3], ny)
    z = np.linspace(grid_bounds[4], grid_bounds[5], nz)
    
    interpolator = RegularGridInterpolator((x, y, z), field, bounds_error=False, fill_value=0.0)
    return interpolator(point)[0]