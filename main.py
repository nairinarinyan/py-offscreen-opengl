from OpenGL.GL import *
import numpy as np
import glfw
import importlib
from PIL import Image
from os import environ

from postprocessing import outline_kernel, blur_kernel, identity_kernel, emboss_kernel
from painter import draw_quad
from image import load_image, save_image
from native_window import create_window_context, main_loop
from utils import load_shaders, load_textures

is_offscreen = environ.get('PYOPENGL_PLATFORM') == 'egl'

diffuse_img_data, width, height = load_image('./images/scene.jpg')
meta_img_data = load_image('./images/meta.jpg')[0]
uv_img_data = load_image('./images/uv.png')[0]

visible_width = round(width * .5)
visible_height = round(height * .5)

if is_offscreen:
    pbuffer = importlib.import_module('pbuffer', '.create_offscreen_context')
    pbuffer.create_offscreen_context(width, height)
    glViewport(0, 0, width, height)
else:
    window = create_window_context(visible_width, visible_height)
    # window = create_window_context(width, height)
    glViewport(0, 0, visible_width, visible_height)
    # glViewport(0, 0, width, height)

def setup():
    program = load_shaders('texture-quad')
    draw_quad()

    return program

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(1, 1, 1, 1.0)

    glUseProgram(program)

    setup_filter()
    handle_textures()

    glDrawArrays(GL_TRIANGLE_FAN, 0, 4)

def handle_textures():
    for idx, texture_data in enumerate(loaded_textures):
        texture, texture_loc = texture_data

        glUniform1i(texture_loc, idx)
        glActiveTexture(getattr(OpenGL.GL, 'GL_TEXTURE{}'.format(idx)))
        glBindTexture(GL_TEXTURE_2D, texture)

def setup_filter():
    # conv_kernel = identity_kernel
    conv_kernel = blur_kernel
    # conv_kernel = emboss_kernel

    kernel_loc = glGetUniformLocation(program, 'u_kernel')
    texture_size_loc = glGetUniformLocation(program, 'u_texture_size')

    glUniform1fv(kernel_loc, len(conv_kernel), conv_kernel)
    glUniform2f(texture_size_loc, width, height)


program = setup()

# name, image data, has alpha channel
textures_to_load = [
    ('diffuse_texture', diffuse_img_data, False),
    ('meta_texture', meta_img_data, False),
    ('uv_texture', uv_img_data, False)
]

loaded_textures = load_textures(program, width, height, textures_to_load)

if is_offscreen:
    draw()
    save_image(width, height, 'out.png')
else:
    main_loop(window, draw)