from abc import ABC, abstractmethod
from core.entities.image_data import ImageData

class ImageRepository(ABC):
    @abstractmethod
    def load_from_file(self, file_path: str) -> ImageData:
        pass

    @abstractmethod
    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        pass