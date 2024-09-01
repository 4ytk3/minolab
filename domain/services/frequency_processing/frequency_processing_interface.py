from abc import ABC, abstractmethod
from domain.entities.image_data import ImageData
import numpy as np

class FrequencyProcessingInterface(ABC):
    @abstractmethod
    def apply(self, image_data: ImageData) -> ImageData:
        pass

    @abstractmethod
    def make_mask(self, shape: tuple, **kwargs) -> np.ndarray:
        pass
