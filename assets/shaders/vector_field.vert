#version 330 core

in vec3 in_position;

// Atributos por cada instancia (flecha)
in vec3 in_offset;
in vec3 in_vector;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform float u_scale;
uniform vec3 u_base_color;

out vec3 v_color;

void main() {
    float mag = length(in_vector);
    
    // Si el campo es cero, escondemos la flecha colapsándola
    if (mag < 1e-12) {
        gl_Position = vec4(0.0, 0.0, 0.0, 0.0);
        return;
    }

    // Escala de calor: Mezcla el color base con rojo según la intensidad del campo
    float normalized_mag = clamp(mag * 100.0, 0.0, 1.0);
    v_color = mix(u_base_color, vec3(1.0, 0.2, 0.2), normalized_mag);

    vec3 dir = in_vector / mag;
    
    // Matemática para rotar la flecha (que apunta originalmente en +Y) hacia `dir`
    vec3 up = vec3(0.0, 1.0, 0.0);
    vec3 axis = cross(up, dir);
    float sinA = length(axis);
    float cosA = dot(up, dir);
    
    vec3 rotated_pos = in_position;
    if (sinA > 0.001) {
        axis = axis / sinA;
        // Fórmula de rotación de Rodrigues
        rotated_pos = in_position * cosA + cross(axis, in_position) * sinA + axis * dot(axis, in_position) * (1.0 - cosA);
    } else if (cosA < -0.999) {
        rotated_pos = vec3(in_position.x, -in_position.y, -in_position.z);
    }

    // Escala logarítmica para que campos muy fuertes no tapen la pantalla
    vec3 final_pos = in_offset + rotated_pos * log(1.0 + mag) * u_scale; 

    gl_Position = m_proj * m_view * vec4(final_pos, 1.0);
}