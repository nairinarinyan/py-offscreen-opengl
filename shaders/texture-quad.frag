#version 330 core
in vec2 tex_coord;

uniform sampler2D diffuse_texture;
uniform sampler2D meta_texture;
uniform sampler2D uv_texture;

out vec4 frag_color;

void main() {
    vec4 diffuse_color = texture(diffuse_texture, tex_coord);
    vec4 meta_color = texture(meta_texture, tex_coord);
    vec4 uv_color = texture(uv_texture, tex_coord);

    frag_color = mix(diffuse_color, uv_color, .5);
}
