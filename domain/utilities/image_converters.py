import cv2
import numpy as np
from domain.entities.image_data import ImageData

def rgb2gray(image_data: ImageData) -> ImageData:
    return ImageData(
        image=cv2.cvtColor(image_data.get_image().astype(np.uint8)),
        format=image_data.get_format(),
        space='grayscale'
    )

def fft(image: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(image))

def ifft(image: np.ndarray) -> np.ndarray:
    return np.abs(np.fft.ifft2(np.fft.fftshift(image)))
