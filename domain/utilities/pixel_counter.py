import numpy as np

def pixel_counter(image: np.ndarray, color: list=[0, 0, 255]):
    counter = 0
    color = np.array(color)
    height, width = image.shape[0], image.shape[1]
    for i in range(height):
        for j in range(width):
            pixel = image[i, j]
            if (pixel == color).all():
                counter += 1
    return counter