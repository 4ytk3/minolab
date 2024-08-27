from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository
from PIL import Image
import numpy as np

class FileImageRepository(ImageRepository):
    def save(self, image_data: ImageData, path: str, format: str):
        image = Image.fromarray(image_data.get_data())
        image.save(path, format=format)

    def load(self, path: str) -> ImageData:
        image = Image.open(path)
        image_data = np.array(image)
        return ImageData(data=image_data)
