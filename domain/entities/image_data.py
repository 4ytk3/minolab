from typing import Tuple
import numpy as np

class ImageData:
    def __init__(self, filename: str, data: np.ndarray, format: str = "JPEG", color_space: str = "RGB", ):
        if not isinstance(data, np.ndarray):
            raise ValueError("data must be a numpy ndarray")
        self.filename = filename
        self.data = data
        self.format = format
        self.color_space = color_space

    def get_filename(self) -> str:
        return self.filename

    def get_data(self) -> np.ndarray:
        return self.data

    def get_format(self) -> str:
        return self.format

    def get_color_space(self) -> str:
        return self.color_space

    def get_size(self) -> Tuple[int, int]:
        if len(self.data.shape) >= 2:
            return self.data.shape[:2]
        else:
            raise ValueError("Invalid image data shape")

    def __repr__(self) -> str:
        return f"ImageData(size={self.get_size()}, format={self.format}, colorspace={self.color_space})"
