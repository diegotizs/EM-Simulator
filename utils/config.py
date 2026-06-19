"""Configuración global de la aplicación."""

# Grilla de campo
GRID_RESOLUTION = 20          # Puntos por eje (20 = grilla 20x20x20)
GRID_BOUNDS = (-1.0, 1.0,     # x_min, x_max en metros
               -1.0, 1.0,     # y_min, y_max en metros
               -1.0, 1.0)     # z_min, z_max en metros

# Simulación
DEFAULT_DT = 1e-10            # Paso de tiempo por defecto en segundos
MAX_PARTICLE_TRAIL = 200      # Máximo de posiciones en el trail de un electrón

# Visualización
VECTOR_COLOR_B = (0.2, 0.5, 1.0)     # Azul para campo B
VECTOR_COLOR_E = (1.0, 0.6, 0.1)     # Naranja para campo E
VECTOR_COLOR_FORCE = (0.2, 0.9, 0.3) # Verde para J×B
BACKGROUND_COLOR = (0.05, 0.05, 0.1) # Fondo casi negro, azul muy oscuro
ELECTRON_COLOR = (0.4, 0.7, 1.0)     # Azul claro para electrones
SELECTED_OUTLINE_COLOR = (1.0, 0.85, 0.0)  # Amarillo para selección

# Render
TARGET_FPS = 60
FIELD_LINE_STEPS = 500        # Pasos de integración por línea de campo
FIELD_LINE_STEP_SIZE = 0.01   # Tamaño de paso para trazar líneas de campos