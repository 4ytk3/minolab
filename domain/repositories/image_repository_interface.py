from abc import ABC, abstractmethod
from domain.entities.image_data import ImageData

class ImageRepositoryInterface(ABC):
    @abstractmethod
    def load_image(self, file_path: str) -> ImageData:
        pass

    @abstractmethod
    def save_image(self, image_data: ImageData, file_path: str) -> None:
        pass