from typing import Tuple
import numpy as np

class ImageData:
    def __init__(self, image: np.ndarray, format: str = "jpg", space: str = "RGB"):
        self.image = image
        self.format = format
        self.space = space

    def get_image(self) -> np.ndarray:
        return self.image

    def get_format(self) -> str:
        return self.format

    def get_space(self) -> str:
        return self.space

    def __repr__(self) -> str:
        return f"ImageData(name={self.name}, format={self.format}, space={self.space})"