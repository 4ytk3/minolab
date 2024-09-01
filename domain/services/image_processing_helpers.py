import cv2
import numpy as np
from domain.entities.image_data import ImageData

def convert_to_grayscale(image_data: ImageData) -> ImageData:
    if image_data.get_color_space() != "grayscale":
        gray_image = cv2.cvtColor(image_data.get_data(), cv2.COLOR_BGR2GRAY)
        return ImageData(data=gray_image, format=image_data.get_format(), color_space="grayscale")
    return image_data

def apply_fft(image_data: np.ndarray) -> np.ndarray:
    return np.fft.fftshift(np.fft.fft2(image_data))

def apply_ifft(frequency_data: np.ndarray) -> np.ndarray:
    return np.abs(np.fft.ifft2(np.fft.ifftshift(frequency_data)))
