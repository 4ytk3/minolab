from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository
import numpy as np
from PIL import Image

class FileImageRepository(ImageRepository):
    def load_from_file(self, file_path: str) -> ImageData:
        try:
            img = Image.open(file_path)
            format = img.format
            if img.mode == 'RGB':
                # RGB画像をグレースケールに変換
                img = img.convert('L')
            data = np.array(img)
            return ImageData(data=data, format=format)
        except Exception as e:
                    raise ValueError(f"Failed to read image from {file_path}: {e}")

    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        try:
            img = Image.fromarray(image_data.get_data())
            img.save(file_path, format=image_data.get_format())
        except Exception as e:
            raise ValueError(f"Failed to save image to {file_path}: {e}")
