import cv2
import numpy as np
from domain.config.frequency_processing_types import FrequencyProcessingTypes
from domain.services.processing_registry import ProcessingRegistry
from domain.services.frequency_processing.frequency_processing_interface import FrequencyProcessingInterface
from domain.services.image_processing_helpers import apply_fft, apply_ifft

class FFT(FrequencyProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray) -> np.ndarray:
        fft_image = apply_fft(gray_image)

    def make_mask(self, shape: tuple, **kwargs) -> np.ndarray:
        height, width = shape
        mask = np.ones([height, width], dtype=np.uint8)
        return mask

class LowpassFilter(FrequencyProcessingInterface):
    def apply(self, image_data: ImageData, radius: int = 90) -> ImageData:
        gray_image = image_data.get_data()
        fft_image = apply_fft(gray_image)
        mask = self.make_mask(fft_image.shape, radius=radius)
        fft_image = fft_image * mask
        ifft_image = apply_ifft(fft_image)
        return ImageData(data=ifft_image.astype(np.float32), format=image_data.get_format(), color_space=image_data.get_color_space())

        shifted_fft[shifted_fft == 0] = np.finfo(float).eps
        return 20*np.log(np.abs(shifted_fft)).astype(np.float32)

    def make_mask(self, shape: tuple, radius: int = 90) -> np.ndarray:
        height, width = shape
        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.circle(mask, (width//2, height//2), radius=radius, color=1, thickness=-1)
        return mask

class HighpassFilter(FrequencyProcessingInterface):
    def apply(self, image_data: ImageData, radius: int = 30) -> ImageData:
        gray_image = image_data.get_data()

        # FFTを適用
        fshift = apply_fft(gray_image)

        # マスクの作成
        mask = self.make_mask(gray_image.shape, radius=radius)

        # マスク適用
        fshift = fshift * mask

        # IFFTを適用して元の画像に戻す
        img_back = apply_ifft(fshift)

        return ImageData(data=img_back.astype(np.float32), format=image_data.get_format(), color_space=image_data.get_color_space())

    def make_mask(self, shape: tuple, radius: int = 30) -> np.ndarray:
        rows, cols = shape
        center = (rows // 2, cols // 2)
        mask = np.ones((rows, cols), np.uint8)
        cv2.circle(mask, center, radius, 0, thickness=-1)
        return mask