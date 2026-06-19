#version 330 core

in vec3 in_position;
in vec3 in_offset;
in vec3 in_vector;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform float u_scale;
uniform vec3 u_base_color;

out vec3 v_color;

void main() {
    float mag = length(in_vector);
    
    if (mag < 1e-12) {
        gl_Position = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }

    // 1. Mejoramos la sensibilidad del color multiplicando por un factor gigante
    float normalized_mag = clamp(mag * 5000000.0, 0.0, 1.0);
    
    // Si es débil toma el color base (amarillo), si es muy fuerte se vuelve rojo
    v_color = mix(u_base_color, vec3(1.0, 0.2, 0.2), normalized_mag);

    vec3 dir = in_vector / mag;
    
    vec3 up = vec3(0.0, 1.0, 0.0);
    vec3 axis = cross(up, dir);
    float sinA = length(axis);
    float cosA = dot(up, dir);
    
    vec3 rotated_pos = in_position;
    if (sinA > 0.001) {
        axis = axis / sinA;
        rotated_pos = in_position * cosA + cross(axis, in_position) * sinA + axis * dot(axis, in_position) * (1.0 - cosA);
    } else if (cosA < -0.999) {
        rotated_pos = vec3(in_position.x, -in_position.y, -in_position.z);
    }

    // 2. TRUCO VISUAL: Forzamos un tamaño casi constante (0.08) para todas las flechas
    // Añadimos un pequeño bono de tamaño (+0.04) si la magnitud es alta
    float visual_length = 0.08 + (normalized_mag * 0.04);
    vec3 final_pos = in_offset + (rotated_pos * visual_length);

    gl_Position = m_proj * m_view * vec4(final_pos, 1.0);
}