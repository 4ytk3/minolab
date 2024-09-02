import cv2
import numpy as np
from domain.config.spatial_processing_types import SpatialProcessingTypes
from domain.services.processing_registry import ProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# 閾値二値化
@ProcessingRegistry.register(SpatialProcessingTypes.THRESHOLD_BINARIZATION)
class ThresholdBinarizationFilter(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, threshold: int = 127) -> np.ndarray:
        _, binarized_image = cv2.threshold(src=gray_image, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
        return binarized_image

# 大津の二値化
@ProcessingRegistry.register(SpatialProcessingTypes.OTSU_BINARIZATION)
class OtsuBinarizationFilter(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray) -> np.ndarray:
        _, binarized_image = cv2.threshold(src=gray_image, thresh=0, maxval=255, type=cv2.THRESH_OTSU)
        return binarized_image

# 適応的二値化
@ProcessingRegistry.register(SpatialProcessingTypes.ADAPTIVE_BINARIZATION)
class AdaptiveBinarizationFilter(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, kernel_size: int = 11) -> np.ndarray:
        binarized_image = cv2.adaptiveThreshold(src=gray_image, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY, blockSize=kernel_size, C=0)
        return binarized_image
