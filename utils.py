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

    # print(glGetShaderInfoLog(vert_shader))
    # print(glGetShaderInfoLog(frag_shader))

    program = glCreateProgram()
    glAttachShader(program, vert_shader)
    glAttachShader(program, frag_shader)
    glLinkProgram(program)

    # print(glGetProgramInfoLog(program))

    return program