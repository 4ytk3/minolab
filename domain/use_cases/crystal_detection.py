from domain.entities.image_data import ImageData
from domain.services.spatial_processing.binarizations import OtsuBinarization
from domain.services.frequency_processing.peak_detector import PeakDetector
from domain.utilities.image_converters import rgb2gray, gray2rgb

import numpy as np

class CrystalDetector:
    def detect_crystal(self, image_data: ImageData):
        original_image = image_data.get_image().copy()
        gray_data = rgb2gray(image_data)

        peak_detector = PeakDetector()
        otsu_binarization = OtsuBinarization()
        detect_peak_image, detect_crystal_image = peak_detector.apply(
            gray_image = gray_data.get_image(),
            exclude_radius = 30,
            radius = 3,
            peak_threshold = 0.8
        )
        binarization_image = otsu_binarization.apply(detect_crystal_image)
        binarization_rgb = gray2rgb(ImageData(image=binarization_image, format=gray_data.get_format(), space=gray_data.get_space()))

        mask = np.all(binarization_rgb.get_image() == [255, 255, 255], axis=-1)
        original_image[mask] = [0, 0, 255]

        return ImageData(image=original_image, format=image_data.get_format(), space="rgb")
