"""Dibuja representaciones visuales del campo electromagnético usando OpenGL."""
import moderngl
import numpy as np
from physics.em_fields import make_grid
from utils.config import GRID_BOUNDS, GRID_RESOLUTION

class FieldRenderer:
    def __init__(self, ctx: moderngl.Context):
        self.ctx = ctx
        
        # Cargar los shaders que acabamos de crear
        with open("assets/shaders/vector_field.vert", "r") as f:
            vs = f.read()
        with open("assets/shaders/vector_field.frag", "r") as f:
            fs = f.read()
            
        self.program = self.ctx.program(vertex_shader=vs, fragment_shader=fs)
        
        # Geometría base de la flecha (Línea central + punta en V)
        verts = np.array([
            0.0, 0.0, 0.0,   0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,  -0.1, 0.8, 0.0,
            0.0, 1.0, 0.0,   0.1, 0.8, 0.0,
            0.0, 1.0, 0.0,   0.0, 0.8,-0.1,
            0.0, 1.0, 0.0,   0.0, 0.8, 0.1
        ], dtype='f4')
        self.vbo_geom = self.ctx.buffer(verts)
        
        # Calculamos la grilla base una sola vez por rendimiento
        self.grid_points = make_grid(GRID_BOUNDS, GRID_RESOLUTION)
        
        # Buffer dinámico para las posiciones e intensidades del campo
        max_instances = len(self.grid_points)
        self.vbo_instances = self.ctx.buffer(reserve=max_instances * 24)
        
        # Empaquetamos todo en un VAO (Vertex Array Object)
        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo_geom, '3f', 'in_position'),
                (self.vbo_instances, '3f 3f/i', 'in_offset', 'in_vector')
            ]
        )

    def draw_vectors(self, field: np.ndarray, color: tuple, scale: float, density: int) -> None:
        """Dibuja el campo como flechas 3D sobre la grilla."""
        # Aplanar array si el motor físico lo devolvió en 4D
        if field.ndim == 4:
            field = field.reshape(-1, 3)
            
        # Filtro de densidad (sliders de la UI)
        step = max(1, 6 - density)
        f_sub = field[::step]
        p_sub = self.grid_points[::step]
        
        # Máscara para ignorar vectores de campo cero y no saturar la GPU
        mags = np.linalg.norm(f_sub, axis=1)
        mask = mags > 1e-12
        f_active = f_sub[mask]
        p_active = p_sub[mask]
        
        if len(f_active) == 0:
            return

        # Mandamos los datos a la tarjeta gráfica
        data = np.hstack((p_active, f_active)).astype('f4').tobytes()
        self.vbo_instances.write(data)
        
       # Actualizamos variables de estado
       # self.program['u_scale'].value = scale#        # type: ignore
        self.program['u_base_color'].value = color   # type: ignore
        
        # ¡Magia instanciada! (GL_LINES es súper ligero)
        self.vao.render(moderngl.LINES, instances=len(f_active))

    def draw_fieldlines(self, field: np.ndarray, color: tuple, n_lines: int) -> None:
        pass # Se implementará en la Fase 6

    def draw_cross_product(self, J: np.ndarray, B: np.ndarray) -> None:
        pass # Se implementará en la Fase 6

    def draw_colormap_volume(self, field: np.ndarray) -> None:
        pass # Se implementará en la Fase 6