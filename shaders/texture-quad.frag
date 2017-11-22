#version 330 core
in vec2 tex_coord;

uniform sampler2D diffuse_sampler;
uniform sampler2D meta_sampler;

out vec4 frag_color;

void main() {
    vec4 diffuse_color = texture(diffuse_sampler, tex_coord);
    vec4 meta_color = texture(meta_sampler, tex_coord);

    frag_color = mix(diffuse_color, meta_color, .5);
}
