import cv2
import numpy as np
from domain.entities.image_data import ImageData

def rgb2gray(image_data: ImageData) -> ImageData:
    return ImageData(
        image = cv2.cvtColor(image_data.get_image().astype(np.uint8), cv2.COLOR_RGB2GRAY),
        format = image_data.get_format(),
        space = 'grayscale'
    )

def gray2rgb(image_data: ImageData) -> ImageData:
    return ImageData(
        image = cv2.cvtColor(image_data.get_image().astype(np.uint8), cv2.COLOR_GRAY2RGB),
        format = image_data.get_format(),
        space = 'rgb'
    )

def fft(image: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(image))

def get_spectrum(shifted_fft: np.ndarray) -> np.ndarray:
    return 20 * np.log(np.abs(shifted_fft)).astype(np.float32)

def ifft(shifted_fft: np.ndarray) -> np.ndarray:
    return np.abs(np.fft.ifft2(np.fft.fftshift(shifted_fft))).astype(np.uint8)
