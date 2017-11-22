from OpenGL.GL import *
import numpy as np

def draw_quad():
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