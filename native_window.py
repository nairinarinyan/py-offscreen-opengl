import glfw
from OpenGL.GL import *

def create_window_context(width, height):
    glfw.init()
    fullscreen = False

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(width, height, "The Window", glfw.get_primary_monitor() if fullscreen else None, None)
    glfw.make_context_current(window)

    return window

def main_loop(window, draw):
    while not glfw.window_should_close(window):
        draw()
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glfw.terminate()
