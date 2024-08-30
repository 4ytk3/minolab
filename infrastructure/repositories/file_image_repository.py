from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository
from infrastructure.image_reader import ImageReader
from infrastructure.image_writer import ImageWriter

class FileImageRepository(ImageRepository):
    def load_from_file(self, file_path: str) -> ImageData:
        return ImageReader.read_image(file_path)

    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        ImageWriter.write_image(image_data, file_path)
