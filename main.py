from OpenGL.GL import *
import numpy as np
import glfw
import importlib
from PIL import Image
from os import environ

from painter import draw_quad
from image import load_image, save_image
from native_window import create_window_context, main_loop
from utils import load_shaders, load_textures

is_offscreen = environ.get('PYOPENGL_PLATFORM') == 'egl'

width, height, diffuse_img_data = load_image('./images/scene.jpg')
_, _ , meta_img_data = load_image('./images/meta.jpg')

visible_width = round(width * .5)
visible_height = round(height * .5)

if is_offscreen:
    pbuffer = importlib.import_module('pbuffer', '.create_offscreen_context')
    pbuffer.create_offscreen_context(width, height)
    glViewport(0, 0, width, height)
else:
    window = create_window_context(visible_width, visible_height)
    glViewport(0, 0, visible_width, visible_height)

def setup():
    program = load_shaders('texture-quad')
    draw_quad()

    return program

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1.0)

    glUseProgram(program)

    glUniform1i(diffuse_sampler_loc, 0)
    glUniform1i(meta_sampler_loc, 1)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, diffuse_texture)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, meta_texture)

    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

program = setup()

diffuse_data, meta_data = load_textures(program, width, height, diffuse_img_data, meta_img_data)

diffuse_texture, diffuse_sampler_loc = diffuse_data
meta_texture, meta_sampler_loc = meta_data

if is_offscreen:
    draw()
    save_image(width, height, 'out.png')
else:
    main_loop(window, draw)