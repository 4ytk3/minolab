from abc import ABC, abstractmethod
from core.entities.image_data import ImageData

class ImageRepository(ABC):
    @abstractmethod
    def save(self, image_data: ImageData, path: str, format: str):
        pass

    @abstractmethod
    def load(self, path: str) -> ImageData:
        pass
