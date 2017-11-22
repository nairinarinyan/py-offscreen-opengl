from OpenGL.GL import *

def load_shaders(name):
    with open('shaders/{0}.vert'.format(name), 'r') as vert_shader_file:
        vert_shader_src = vert_shader_file.read()

    with open('shaders/{0}.frag'.format(name), 'r') as frag_shader_file:
        frag_shader_src = frag_shader_file.read()

    vert_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vert_shader, vert_shader_src)
    glCompileShader(vert_shader)

    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(frag_shader, frag_shader_src)
    glCompileShader(frag_shader)

    print(glGetShaderInfoLog(vert_shader))
    print(glGetShaderInfoLog(frag_shader))

    program = glCreateProgram()
    glAttachShader(program, vert_shader)
    glAttachShader(program, frag_shader)
    glLinkProgram(program)

    print(glGetProgramInfoLog(program))

    return program

def load_textures(program, width, height, diffuse_img_data, meta_img_data):
    [diffuse_texture, meta_texture] = glGenTextures(2)

    glBindTexture(GL_TEXTURE_2D, diffuse_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, diffuse_img_data) 
    glBindTexture(GL_TEXTURE_2D, 0)

    glBindTexture(GL_TEXTURE_2D, meta_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, meta_img_data) 
    glBindTexture(GL_TEXTURE_2D, 1)

    diffuse_sampler_loc = glGetUniformLocation(program, 'diffuse_sampler')
    meta_sampler_loc = glGetUniformLocation(program, 'meta_sampler')

    ret = [
        (diffuse_texture, diffuse_sampler_loc),
        (meta_texture, meta_sampler_loc)
    ]

    return ret
