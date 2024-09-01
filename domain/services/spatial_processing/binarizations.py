import cv2
import numpy as np
from domain.config.category_types import CategoryTypes
from domain.services.spatial_processing.spatial_processing_registry import SpatialProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 閾値二値化
@SpatialProcessingRegistry.register(CategoryTypes.THRESHOLD_BINARIZATION)
class ThresholdBinarizationFilter(SpatialProcessingInterface):
    def apply(self, gray_image: np.ndarray, threshold: int = 127) -> np.ndarray:
        _, binarized_image = cv2.threshold(src=gray_image, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
        return binarized_image

# 大津の二値化
@SpatialProcessingRegistry.register(CategoryTypes.OTSU_BINARIZATION)
class OtsuBinarizationFilter(SpatialProcessingInterface):
    def apply(self, gray_image: np.ndarray) -> np.ndarray:
        _, binarized_image = cv2.threshold(src=gray_image, thresh=0, maxval=255, type=cv2.THRESH_OTSU)
        return binarized_image

# 適応的二値化
@SpatialProcessingRegistry.register(CategoryTypes.ADAPTIVE_BINARIZATION)
class AdaptiveBinarizationFilter(SpatialProcessingInterface):
    def apply(self, gray_image: np.ndarray, kernel_size: int = 11) -> np.ndarray:
        binarized_image = cv2.adaptiveThreshold(src=gray_image, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=kernel_size, C=0)
        return binarized_image
