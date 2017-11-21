from OpenGL.GL import *
import numpy as np
import glfw
import importlib
from os import environ

from image import save_image
from native_window import create_window_context, main_loop
from utils import load_shaders

width = 1080
height = 720

is_offscreen = environ.get('PYOPENGL_PLATFORM') == 'egl'

if is_offscreen:
    pbuffer = importlib.import_module('pbuffer', '.create_offscreen_context')
    pbuffer.create_offscreen_context(width, height)
else:
    window = create_window_context(width, height)

def setup():
    program = load_shaders('first')

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

    # setup buffers (vao, vbos) and fill data
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

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

    glViewport(0, 0, width, height)
    
    return program

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1.0)

    glUseProgram(program)

    glDrawArrays(GL_TRIANGLES, 0, 3)

program = setup()

if is_offscreen:
    draw()
    save_image(width, height, 'out.png')
else:
    main_loop(window, draw)