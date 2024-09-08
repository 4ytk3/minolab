from domain.entities.image_data import ImageData
from domain.services.spatial_processing.binarizations import OtsuBinarization
from domain.services.frequency_processing.peak_detector import PeakDetector
from domain.utilities.image_converters import rgb2gray, get_spectrum, fft

import numpy as np

class CrystalDetector:
    def detect_crystal(self, image_data: ImageData):
        original_image = image_data.get_image().copy()
        gray_data = rgb2gray(image_data)
        fft_image = get_spectrum(fft(gray_data.get_image()))

        peak_detector = PeakDetector()
        otsu_binarization = OtsuBinarization()
        detect_peak_image, detect_crystal_image = peak_detector.apply(gray_image = gray_data.get_image(), exclude_radius = 30, radius = 3, peak_threshold = 0.8)
        binarization_image = otsu_binarization.apply(detect_crystal_image)

        colorized_image = self.colorize_image(original_image=original_image, binarization_image=binarization_image, color=[0, 0, 255])

        return (
            ImageData(image=fft_image, format=image_data.get_format(), space="frequency"),
            ImageData(image=detect_peak_image, format=image_data.get_format(), space="frequency"),
            ImageData(image=binarization_image, format=image_data.get_format(), space="grayscale"),
            ImageData(image=colorized_image, format=image_data.get_format(), space="rgb")
        )

    def colorize_image(self, original_image: np.ndarray, binarization_image: np.ndarray, color: list = [0, 0, 255]) -> np.ndarray:
        mask = (binarization_image == 255)
        original_image[mask] = color

        return original_image