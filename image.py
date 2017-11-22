from PIL import Image
from OpenGL.GL import *
import numpy as np

# read and save image
def save_image(width, height, image_name):
    buffer = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE);

    image = Image.frombytes(mode="RGB", size=(width, height), data=buffer)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    image.save(image_name)

def load_image(imagePath):
    image = Image.open(imagePath)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(list(image.getdata()), np.uint8)

    width, height = image.size
    return width, height, img_data