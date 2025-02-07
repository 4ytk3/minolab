from domain.config.processing_types import FrequencyProcessingTypes
from domain.services.processing_registry import FrequencyProcessingRegistry
from domain.services.frequency_processing.frequency_processing_interface import FrequencyProcessingInterface
from domain.utilities.image_converters import fft, get_spectrum, ifft

import cv2
import numpy as np

class FrequencyBaseFilter(FrequencyProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, **kwargs) -> np.ndarray:
        shifted_fft = fft(gray_image)
        mask = self.make_mask(shifted_fft.shape, **kwargs)
        masked_fft = shifted_fft * mask
        masked_fft[masked_fft == 0] = np.finfo(float).eps

        fft_image = get_spectrum(shifted_fft=shifted_fft)
        ifft_image = ifft(shifted_fft=masked_fft).astype(np.uint8)

        return fft_image, ifft_image

    def make_mask(self, shape: tuple, **kwargs) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement make_mask method")

@FrequencyProcessingRegistry.register(FrequencyProcessingTypes.LOWPASS_FILTER)
class LowpassFilter(FrequencyBaseFilter):
    def make_mask(self, shape: tuple, radius: int = 90) -> np.ndarray:
        height, width = shape
        mask = np.zeros(shape=shape, dtype=np.uint8)
        cv2.circle(mask, center=(width//2, height//2), radius=radius, color=1, thickness=-1)
        return mask

@FrequencyProcessingRegistry.register(FrequencyProcessingTypes.HIGHPASS_FILTER)
class HighpassFilter(FrequencyBaseFilter):
    def make_mask(self, shape: tuple, radius: int = 30) -> np.ndarray:
        height, width = shape
        mask = np.ones(shape=shape, dtype=np.uint8)
        cv2.circle(mask, center=(width//2, height//2), radius=radius, color=0, thickness=-1)
        return mask

@FrequencyProcessingRegistry.register(FrequencyProcessingTypes.BANDPASS_FILTER)
class BandpassFilter(FrequencyBaseFilter):
    def make_mask(self, shape: tuple, outer_radius=150, inner_radius=50):
        height, width = shape
        mask = np.zeros(shape=shape, dtype=np.uint8)
        cv2.circle(mask, center=(width//2, height//2), radius=outer_radius, color=1, thickness=-1)
        cv2.circle(mask, center=(width//2, height//2), radius=inner_radius, color=0, thickness=-1)
        return mask