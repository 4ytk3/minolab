from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository
from PIL import Image
import numpy as np

class FileImageRepository(ImageRepository):
    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        """Save the image data to a file."""
        try:
            img = Image.fromarray(image_data.get_data())
            img.save(file_path, format=image_data.get_format())
        except Exception as e:
            raise ValueError(f"Failed to save image to {file_path}: {e}")

    def load_from_file(self, file_path: str) -> ImageData:
        """Load image data from a file."""
        try:
            img = Image.open(file_path)
            data = np.array(img)
            format = img.format if img.format else "unknown"
            return ImageData(data=data, format=format)
        except Exception as e:
            raise ValueError(f"Failed to load image from {file_path}: {e}")
