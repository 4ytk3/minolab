from PIL import Image

class ImageWriter:
    def write(self, image, path, format):
        image.save(path, format=format)
