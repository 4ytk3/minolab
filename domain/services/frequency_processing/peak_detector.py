from domain.config.processing_types import FrequencyProcessingTypes
from domain.services.processing_registry import FrequencyProcessingRegistry
from domain.services.frequency_processing.frequency_processing_interface import FrequencyProcessingInterface
from domain.utilities.image_converters import fft, ifft

import cv2
import numpy as np
from skimage.feature import peak_local_max

@FrequencyProcessingRegistry.register(FrequencyProcessingTypes.PEAK_DETECTOR)
class PeakDetector(FrequencyProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, exclude_radius: int = 30, radius: int = 3, min_distance=10, threshold_abs=None, peak_threshold: float = 0.8, **kwargs) -> np.ndarray:
        shifted_fft = fft(gray_image)
        shifted_fft = self.remove_low_frequencies(shifted_fft, exclude_radius=exclude_radius)
        peak_image = self.detect_peaks(shifted_fft, min_distance=min_distance, threshold_abs=threshold_abs, peak_threshold=peak_threshold)
        mask = self.make_mask(peak_image, shifted_fft.shape, radius=radius)
        masked_fft = shifted_fft * mask
        masked_fft[masked_fft == 0] = np.finfo(float).eps

        fft_image = 20 * np.log(np.abs(masked_fft)).astype(np.float32)
        ifft_image = ifft(masked_fft).astype(np.uint8)

        return fft_image, ifft_image

    def remove_low_frequencies(self, shifted_fft: np.ndarray, exclude_radius: int = 1):
        height, width = shifted_fft.shape
        mask = np.ones((height, width), dtype=np.uint8)
        cv2.circle(mask, (width//2, height//2), radius=exclude_radius, color=0, thickness=-1)
        return shifted_fft * mask

    def make_mask(self, peak_image: np.ndarray, shape: tuple, radius: int = 3) -> np.ndarray:
        mask = np.zeros(shape, dtype=np.uint8)
        indices = np.dstack(np.where(peak_image == 1))[0]
        for index in indices:
            cv2.circle(mask, center=(index[1], index[0]), radius=radius, color=1, thickness=-1)
        return mask

    def detect_peaks(self, shifted_fft: np.ndarray, min_distance=10, threshold_abs=None, peak_threshold: float = 0.8):
        magnitude_spectrum = np.abs(shifted_fft)
        coordinates = peak_local_max(magnitude_spectrum, min_distance=min_distance, threshold_abs=threshold_abs)
        filtered_coordinates = [
            coord for coord in coordinates
            if not (coord[1] == shifted_fft.shape[1]//2 or coord[0] == shifted_fft.shape[0]//2)
        ]

        if len(filtered_coordinates) == 0:
            return np.zeros_like(magnitude_spectrum)

        peak_max = max([magnitude_spectrum[coord[0], coord[1]] for coord in filtered_coordinates])
        peak_image = np.zeros_like(magnitude_spectrum)
        for coord in filtered_coordinates:
            if magnitude_spectrum[coord[0], coord[1]] >= peak_max * peak_threshold:
                peak_image[coord[0], coord[1]] = 1

        return peak_image
