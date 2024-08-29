from core.entities.image_data import ImageData
import numpy as np
from PIL import Image

class ImageReader:
    @staticmethod
    def read_image(file_path: str) -> ImageData:
        try:
            img = Image.open(file_path)
            data = np.array(img)
            return ImageData(data=data, format=img.format)
        except Exception as e:
            raise ValueError(f"Failed to read image from {file_path}: {e}")