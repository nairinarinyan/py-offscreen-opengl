import numpy as np
from OpenGL import arrays
from OpenGL.GL import *
from OpenGL.EGL import *
from PIL import Image
from ctypes import *

width = 1080
height = 720

# get display, setup EGL
dpy = eglGetDisplay(EGL_DEFAULT_DISPLAY)

eglInitialize(dpy, None, None)

# setup context and pixel buffer for offscreen rendering
egl_config_attribs = [
    EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
    EGL_BLUE_SIZE, 8,
    EGL_GREEN_SIZE, 8,
    EGL_RED_SIZE, 8,
    EGL_ALPHA_SIZE, 8,
    EGL_DEPTH_SIZE, 8,
    EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
    EGL_NONE
]

p_buffer_attribs = [
    EGL_WIDTH, width,
    EGL_HEIGHT, height,
    EGL_NONE
]

egl_attribs_list = arrays.GLintArray.asArray(egl_config_attribs)
p_buffer_attribs_list = arrays.GLintArray.asArray(p_buffer_attribs)

num_configs = ctypes.c_long()
egl_configs = (EGLConfig * 2)()

eglChooseConfig(dpy, egl_attribs_list, egl_configs, 2, num_configs)
eglBindAPI(EGL_OPENGL_API)

surf = eglCreatePbufferSurface(dpy, egl_configs[0], p_buffer_attribs_list)
ctx = eglCreateContext(dpy, egl_configs[0], EGL_NO_CONTEXT, None)

eglMakeCurrent(dpy, surf, surf, ctx)

# compile, link and load shaders
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

# declare some data
position_data = np.array([
     0,  .6,
   -.5, -.3,
    .5, -.3,
], np.float32)

color_data = np.array([
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0
], np.float32)

# start the party
program = load_shaders('first')

# setup buffers (vao, vbos) and fill data
vao = glGenVertexArrays(1)
glBindVertexArray(vao);

itemsize = np.dtype('float32').itemsize

[position_vbo, color_vbo] = glGenBuffers(2)

glBindBuffer(GL_ARRAY_BUFFER, position_vbo)
glBufferData(GL_ARRAY_BUFFER, itemsize * position_data.size, position_data, GL_STATIC_DRAW)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
glBufferData(GL_ARRAY_BUFFER, itemsize * color_data.size, color_data, GL_STATIC_DRAW)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(1)

# draw
glViewport(0, 0, width, height)
glClear(GL_COLOR_BUFFER_BIT)
glClearColor(1, 1, 1, 1.0)

glUseProgram(program)

glBindVertexArray(vao);
glDrawArrays(GL_TRIANGLES, 0, 3)

# read and save image
buffer = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE);
image = Image.frombytes(mode="RGB", size=(width, height), data=buffer)
image = image.transpose(Image.FLIP_TOP_BOTTOM)

image.save('out.png')