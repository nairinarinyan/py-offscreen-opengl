import numpy as np

outline_kernel = np.array([
    -1, -1, -1,
    -1, 8, -1,
    -1, -1, -1
], np.float32)

blur_kernel = np.array([
    1/9, 1/9, 1/9,
    1/9, 1/9, 1/9,
    1/9, 1/9, 1/9
], np.float32)

identity_kernel = np.array([
    0, 0, 0,
    0, 1, 0,
    0, 0, 0
], np.float32)

emboss_kernel = np.array([
    -2, -1, 0,
    -1, 1, 1,
    0, 1, 2
], np.float32)