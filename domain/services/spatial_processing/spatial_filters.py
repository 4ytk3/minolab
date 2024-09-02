import cv2
import numpy as np
from domain.config.spatial_processing_types import SpatialProcessingTypes
from domain.services.processing_registry import ProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 平均値フィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.AVERAGE_FILTER)
class AverageFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        return cv2.blur(src=image, ksize=(kernel_size, kernel_size))

# 中央値フィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.MEDIAN_FILTER)
class MedianFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        return cv2.medianBlur(src=image, ksize=kernel_size)

# ガウシアンフィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.GAUSSIAN_FILTER)
class GaussianFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaX: int = 3) -> np.ndarray:
        return cv2.GaussianBlur(src=image, ksize=(kernel_size, kernel_size), sigmaX=sigmaX)

# バイラテラルフィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.BILATERAL_FILTER)
class BilateralFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaColor=50, sigmaSpace=50) -> np.ndarray:
        return cv2.bilateralFilter(src=image, d=kernel_size, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
