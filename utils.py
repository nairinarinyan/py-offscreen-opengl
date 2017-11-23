from OpenGL.GL import *

def load_shaders(name):
    with open('shaders/{}.vert'.format(name), 'r') as vert_shader_file:
        vert_shader_src = vert_shader_file.read()

    with open('shaders/{}.frag'.format(name), 'r') as frag_shader_file:
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

def load_textures(program, width, height, textures_to_load):
    num_textures = len(textures_to_load)
    ret = []

    textures = glGenTextures(num_textures)

    for idx, texture_to_load in enumerate(textures_to_load):
        texture_name, texture_data = texture_to_load
        texture = textures[idx]

        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data) 
        glBindTexture(GL_TEXTURE_2D, idx)

        texture_loc = glGetUniformLocation(program, texture_name)

        ret.append((texture, texture_loc))
        
    return ret
    # glBindTexture(GL_TEXTURE_2D, meta_texture)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, meta_img_data) 
    # glBindTexture(GL_TEXTURE_2D, 1)

    # diffuse_texture_loc = glGetUniformLocation(program, 'diffuse_texture')
    # meta_texture_loc = glGetUniformLocation(program, 'meta_texture')

    # ret = [
    #     (diffuse_texture, diffuse_texture_loc),
    #     (meta_texture, meta_texture_loc)
    # ]
