from OpenGL import arrays
from OpenGL.EGL import *
from ctypes import *

def create_offscreen_context(width, height):
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