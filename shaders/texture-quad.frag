#version 330 core
in vec2 tex_coord;

uniform sampler2D diffuse_texture;
uniform sampler2D meta_texture;
uniform sampler2D uv_texture;

uniform float u_kernel[9];
uniform vec2 u_texture_size;

out vec4 frag_color;

// void main() {
//     vec4 sum = vec4(0.0);
//     vec2 step_size = 1.0/u_texture_size;

//     sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y - step_size.y)) * u_kernel[0];
//     sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y - step_size.y)) * u_kernel[1];
//     sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y - step_size.y)) * u_kernel[2];
    
//     sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y)) * u_kernel[3];
//     sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y)) * u_kernel[4];
//     sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y)) * u_kernel[5];

//     sum += texture(diffuse_texture, vec2(tex_coord.x - step_size.x, tex_coord.y + step_size.y)) * u_kernel[6];
//     sum += texture(diffuse_texture, vec2(tex_coord.x, tex_coord.y + step_size.y)) * u_kernel[7];
//     sum += texture(diffuse_texture, vec2(tex_coord.x + step_size.x, tex_coord.y + step_size.y)) * u_kernel[7];

//     sum.a = 1.0;

//     frag_color = mix(sum, texture(uv_texture, tex_coord), .5);
// }

// uniform sampler2D tex0; 

// GeeXLab built-in uniform, width of
// the current render target
// uniform float rt_w; 
// GeeXLab built-in uniform, height of
// the current render target
// uniform float rt_h; 
// 
// Swirl effect parameters
uniform float radius;
uniform float angle;
vec2 center = u_texture_size / 2;

vec4 PostFX(sampler2D tex, vec2 uv)
{
  vec2 tc = uv * u_texture_size;
  tc -= center;
  float dist = length(tc);
  if (dist < radius) 
  {
    float percent = (radius - dist) / radius;
    float theta = percent * percent * angle * 8.0;
    float s = sin(theta);
    float c = cos(theta);
    tc = vec2(dot(tc, vec2(c, -s)), dot(tc, vec2(s, c)));
  }
  tc += center;

//   vec4 c1 = texture(tex, tc / u_texture_size);
  return texture(uv_texture, tc / u_texture_size);

//   return mix(c1, c2, .5);
}

void main (void)
{
//   vec2 uv = gl_TexCoord[0].st;
  frag_color = PostFX(diffuse_texture, tex_coord);
}
