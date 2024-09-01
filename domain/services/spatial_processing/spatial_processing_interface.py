import numpy as np
from abc import ABC, abstractmethod

class SpatialProcessingInterface(ABC):
    @abstractmethod
    def apply(self, image: np.ndarray) -> np.ndarray:
        pass
