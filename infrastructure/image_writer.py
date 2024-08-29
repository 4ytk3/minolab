from core.entities.image_data import ImageData
from PIL import Image

class ImageWriter:
    @staticmethod
    def write_image(image_data: ImageData, file_path: str) -> None:
        try:
            img = Image.fromarray(image_data.get_data())
            img.save(file_path, format=image_data.get_format())
        except Exception as e:
            raise ValueError(f"Failed to write image to {file_path}: {e}")