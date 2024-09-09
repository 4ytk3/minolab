import cv2
import numpy as np
from domain.config.processing_types import SpatialProcessingTypes
from domain.services.processing_registry import SpatialProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 平均値フィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.AVERAGE_FILTER)
class AverageFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = False

    def apply(self, image: np.ndarray, kernel_size: int = 3, **kwargs) -> np.ndarray:
        filtered_image = cv2.blur(src=image, ksize=(kernel_size, kernel_size))
        return filtered_image

# 中央値フィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.MEDIAN_FILTER)
class MedianFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = False

    def apply(self, image: np.ndarray, kernel_size: int = 3, **kwargs) -> np.ndarray:
        filtered_image = cv2.medianBlur(src=image, ksize=kernel_size)
        return filtered_image

# ガウシアンフィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.GAUSSIAN_FILTER)
class GaussianFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = False

    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaX: int = 3, **kwargs) -> np.ndarray:
        filtered_image = cv2.GaussianBlur(src=image, ksize=(kernel_size, kernel_size), sigmaX=sigmaX)
        return filtered_image

# バイラテラルフィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.BILATERAL_FILTER)
class BilateralFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = False

    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaColor=50, sigmaSpace=50, **kwargs) -> np.ndarray:
        filtered_image = cv2.bilateralFilter(src=image, d=kernel_size, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
        return filtered_image
