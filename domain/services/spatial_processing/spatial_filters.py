import cv2
import numpy as np
from domain.config.category_types import CategoryTypes
from domain.services.spatial_processing.spatial_processing_registry import SpatialProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 平均値フィルタ
@SpatialProcessingRegistry.register(CategoryTypes.AVERAGE_FILTER)
class AverageFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        return cv2.blur(src=image, ksize=(kernel_size, kernel_size))

# 中央値フィルタ
@SpatialProcessingRegistry.register(CategoryTypes.MEDIAN_FILTER)
class MedianFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        return cv2.medianBlur(src=image, ksize=kernel_size)

# ガウシアンフィルタ
@SpatialProcessingRegistry.register(CategoryTypes.GAUSSIAN_FILTER)
class GaussianFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaX: int = 3) -> np.ndarray:
        return cv2.GaussianBlur(src=image, ksize=(kernel_size, kernel_size), sigmaX=sigmaX)

# バイラテラルフィルタ
@SpatialProcessingRegistry.register(CategoryTypes.BILATERAL_FILTER)
class BilateralFilter(SpatialProcessingInterface):
    def apply(self, image: np.ndarray, kernel_size: int = 3, sigmaColor=50, sigmaSpace=50) -> np.ndarray:
        return cv2.bilateralFilter(src=image, d=kernel_size, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
