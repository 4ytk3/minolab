from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository
import numpy as np
from PIL import Image

class FileImageRepository(ImageRepository):
    def load_from_file(self, file_path: str) -> ImageData:
        img = Image.open(file_path)
        if img.mode == 'RGB':
            # RGB画像をグレースケールに変換
            img = img.convert('L')
        data = np.array(img)
        return ImageData(data=data, format='grayscale' if img.mode == 'L' else 'RGB')

    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        img = Image.fromarray(image_data.get_data())
        img.save(file_path, format=image_data.get_format())
