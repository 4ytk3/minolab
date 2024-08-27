from PIL import Image

class ImageReader:
    def read(self, path):
        return Image.open(path)
