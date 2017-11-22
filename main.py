from OpenGL.GL import *
import numpy as np
import glfw
import importlib
from os import environ
from PIL import Image

from image import save_image
from native_window import create_window_context, main_loop
from utils import load_shaders

width = 800
height = 480

is_offscreen = environ.get('PYOPENGL_PLATFORM') == 'egl'

if is_offscreen:
    pbuffer = importlib.import_module('pbuffer', '.create_offscreen_context')
    pbuffer.create_offscreen_context(width, height)
else:
    window = create_window_context(width, height)

def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(list(image.getdata()), np.uint8)
    texture = glGenTextures(1)

    img_width, img_height = image.size

    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data) 
    glBindTexture(GL_TEXTURE_2D, 0)

    tex_sampler_loc = glGetUniformLocation(program, 'tex_sampler')

    return texture, tex_sampler_loc


def setup():
    glViewport(0, 0, width, height)

    program = load_shaders('texture-quad')

    position_data = np.array([
        1, 1,
        -1, 1,
        -1, -1,
        1, -1,
    ], np.float32)

    texture_coord_data = np.array([
        1,1,
        0, 1,
        0, 0,
        1, 0
    ], np.float32)

    # setup buffers (vao, vbos) and fill data
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    itemsize = np.dtype('float32').itemsize

    [pos_vbo, tex_coord_vbo] = glGenBuffers(2)

    glBindBuffer(GL_ARRAY_BUFFER, pos_vbo)
    glBufferData(GL_ARRAY_BUFFER, itemsize * position_data.size, position_data, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, tex_coord_vbo)
    glBufferData(GL_ARRAY_BUFFER, itemsize * texture_coord_data.size, texture_coord_data, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    return program

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1.0)

    glUseProgram(program)

    glUniform1i(tex_sampler_loc, 0)
    glBindTexture(GL_TEXTURE_2D, texture)

    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

program = setup()
texture, tex_sampler_loc = load_texture('./images/scene.jpg')

if is_offscreen:
    draw()
    save_image(width, height, 'out.png')
else:
    main_loop(window, draw)