from typing import Tuple
import numpy as np

class ImageData:
    def __init__(self, data: np.ndarray, format: str = "unknown"):
        if not isinstance(data, np.ndarray):
            raise ValueError("data must be a numpy ndarray")
        self.data = data
        self.format = format

    def get_data(self) -> np.ndarray:
        return self.data

    def get_format(self) -> str:
        return self.format

    def get_size(self) -> Tuple[int, int]:
        if len(self.data.shape) >= 2:
            return self.data.shape[:2]
        else:
            raise ValueError("Invalid image data shape")

    def __repr__(self) -> str:
        return f"ImageData(size={self.get_size()}, format={self.format})"
