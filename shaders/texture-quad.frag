#version 330 core
in vec2 tex_coord;

uniform sampler2D diffuse_texture;
uniform sampler2D meta_texture;
uniform sampler2D uv_texture;

uniform float u_kernel[9];
uniform vec2 u_texture_size;

out vec4 frag_color;

void main() {
    vec4 sum = vec4(0.0);
    vec2 step_size = 1.0/u_texture_size;

    sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y - step_size.y)) * u_kernel[0];
    sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y - step_size.y)) * u_kernel[1];
    sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y - step_size.y)) * u_kernel[2];
    
    sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y)) * u_kernel[3];
    sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y)) * u_kernel[4];
    sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y)) * u_kernel[5];

    sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y + step_size.y)) * u_kernel[6];
    sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y + step_size.y)) * u_kernel[7];
    sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y + step_size.y)) * u_kernel[7];

    sum.a = 1.0;

    frag_color = mix(sum, texture(uv_texture, tex_coord), .5);
}
