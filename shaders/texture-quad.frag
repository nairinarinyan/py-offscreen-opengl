#version 330 core
in vec2 tex_coord;

uniform sampler2D tex_sampler;

out vec4 frag_color;

void main() {
    frag_color = texture(tex_sampler, tex_coord);
    // frag_color = vec4(tex_coord, 1, 1);
}
