"""Escena principal: cámara, ejes, loop de render."""
import moderngl
import numpy as np
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from pyrr import Matrix44

from renderer.field_renderer import FieldRenderer
from physics.em_fields import compute_B_field

class Scene3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ctx = None
        self.field_renderer = None
        
        # Estado de la cámara orbital
        self.camera_distance = 1.5
        self.camera_rot_x = np.pi / 6   # Elevación inicial
        self.camera_rot_y = -np.pi / 4  # Azimut inicial
        self.last_mouse_pos = None
        
        # Datos físicos de la escena
        self.elements = []
        self.B_field = None

    def initializeGL(self):
        """Se llama una sola vez cuando la ventana se crea."""
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST) # Para que las flechas cercanas tapen a las lejanas
        self.ctx.line_width = 2.0

        # Inicializar nuestro dibujante de campos
        self.field_renderer = FieldRenderer(self.ctx)

    def resizeGL(self, w, h):
        """Se llama si el usuario cambia el tamaño de la ventana."""
        self.ctx.viewport = (0, 0, w, h)

    def paintGL(self):
        """El loop de renderizado (se llama en cada frame)."""
        # Limpiar el fondo (un azul muy oscuro/casi negro)
        self.ctx.clear(0.05, 0.05, 0.1)
        
        if not self.elements or self.B_field is None:
            return

        # 1. Calcular posición de la cámara (Coordenadas Esféricas a Cartesianas)
        cam_x = self.camera_distance * np.cos(self.camera_rot_x) * np.sin(self.camera_rot_y)
        cam_y = self.camera_distance * np.sin(self.camera_rot_x)
        cam_z = self.camera_distance * np.cos(self.camera_rot_x) * np.cos(self.camera_rot_y)
        
        # 2. Crear las matrices matemáticas de la cámara
        view = Matrix44.look_at(
            eye=[cam_x, cam_y, cam_z],
            target=[0.0, 0.0, 0.0],
            up=[0.0, 1.0, 0.0]
        )
        proj = Matrix44.perspective_projection(45.0, self.width() / self.height(), 0.1, 100.0)
        
        # 3. Mandar matrices a la tarjeta gráfica
        self.field_renderer.program['m_view'].write(view.astype('f4').tobytes())
        self.field_renderer.program['m_proj'].write(proj.astype('f4').tobytes())
        
        # 4. ¡Dibujar!
        self.field_renderer.draw_vectors(
            field=self.B_field,
            color=(1.0, 0.8, 0.0), # <--- Amarillo brillante para máximo contraste
            scale=1.0,             # (El scale ya no importa tanto con el nuevo shader)
            density=3
        )

    def update_fields(self):
        """Recalcula el campo magnético usando el motor de física."""
        if self.field_renderer is not None:
            self.B_field = compute_B_field(self.elements, self.field_renderer.grid_points)
            self.update() # Fuerza a redibujar el frame

    # --- Controles de la cámara con el ratón ---
    def mousePressEvent(self, event):
        self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.last_mouse_pos:
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()
            
            self.camera_rot_y -= dx * 0.01
            self.camera_rot_x += dy * 0.01
            # Limitar la cámara para que no dé la vuelta completa de cabeza
            self.camera_rot_x = np.clip(self.camera_rot_x, -np.pi/2 + 0.1, np.pi/2 - 0.1)
            
            self.last_mouse_pos = event.position()
            self.update()

    def wheelEvent(self, event):
        self.camera_distance -= event.angleDelta().y() * 0.005
        self.camera_distance = max(0.5, self.camera_distance) # No acercarse más del centro
        self.update()