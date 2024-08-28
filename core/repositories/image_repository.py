from abc import ABC, abstractmethod
from typing import Any
from core.entities.image_data import ImageData

class ImageRepository(ABC):
    @abstractmethod
    def save_to_file(self, image_data: ImageData, file_path: str) -> None:
        """Save the image data to a file."""
        pass

    @abstractmethod
    def load_from_file(self, file_path: str) -> ImageData:
        """Load image data from a file."""
        pass
