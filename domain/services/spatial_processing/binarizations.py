import cv2
import numpy as np
from domain.config.processing_types import SpatialProcessingTypes
from domain.services.processing_registry import SpatialProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 閾値二値化
@SpatialProcessingRegistry.register(SpatialProcessingTypes.THRESHOLD_BINARIZATION)
class ThresholdBinarization(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, threshold: int = 127) -> np.ndarray:
        if not (0 <= threshold <= 255):
            raise ValueError(f"Threshold value {threshold} is out of range. Must be between 0 and 255.")
        _, binarized_image = cv2.threshold(src=gray_image, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
        return binarized_image

# 大津の二値化
@SpatialProcessingRegistry.register(SpatialProcessingTypes.OTSU_BINARIZATION)
class OtsuBinarization(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray) -> np.ndarray:
        _, binarized_image = cv2.threshold(src=gray_image, thresh=0, maxval=255, type=cv2.THRESH_OTSU)
        return binarized_image

# 適応的二値化
@SpatialProcessingRegistry.register(SpatialProcessingTypes.ADAPTIVE_BINARIZATION)
class AdaptiveBinarization(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        binarized_image = cv2.adaptiveThreshold(src=gray_image, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=kernel_size, C=0)
        return binarized_image
