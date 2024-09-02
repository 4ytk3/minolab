import cv2
import numpy as np
from domain.config.spatial_processing_types import SpatialProcessingTypes
from domain.services.processing_registry import ProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# Cannyエッジ検出器
@ProcessingRegistry.register(SpatialProcessingTypes.CANNY_EDGE_DETECTOR)
class CannyEdgeDetector(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, min_val: int = 100, max_val: int = 300) -> np.ndarray:
        return cv2.Canny(image=gray_image, threshold1=min_val, threshold2=max_val, L2gradient=False)

# プレヴィットフィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.PREWITT_FILTER)
class PrewittFilter(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
        kernel_x, kernel_y = self.make_kernel(kernel_size)
        prewitt_x = cv2.filter2D(gray_image, -1, kernel_x)
        prewitt_y = cv2.filter2D(gray_image, -1, kernel_y)
        return np.sqrt(prewitt_x**2 + prewitt_y**2)

    def make_kernel(self, kernel_size: int = 3):
        if kernel_size == 3:
            kernel_x = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
            kernel_y = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        elif kernel_size == 5:
            kernel_x = np.array([[2,2,2,2,2],[1,1,1,1,1],[0,0,0,0,0],[-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2]])
            kernel_y = np.array([[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2]])
        elif kernel_size == 7:
            kernel_x = np.array([[3,3,3,3,3,3,3],[2,2,2,2,2,2,2],[1,1,1,1,1,1,1],[0,0,0,0,0,0,0],[-1,-1,-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2,-2,-2],[-3,-3,-3,-3,-3,-3,-3]])
            kernel_y = np.array([[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3]])
        else:
            print(f"kernel_size={kernel_size} dosen't support")
        return kernel_x, kernel_y

# ソーベルフィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.SOBELFILTER)
class SobelFilter(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, dx=1, dy=1, kernel_size=3, amp=3):
        sobel_x = cv2.Sobel(src=gray_image, ddepth=cv2.CV_8U, dx=dx, dy=dy, ksize=kernel_size) # X方向
        sobel_y = cv2.Sobel(src=gray_image, ddepth=cv2.CV_8U, dx=dx, dy=dy, ksize=kernel_size) # Y方向
        sobel_x = cv2.convertScaleAbs(src=sobel_x, alpha=0.5)
        sobel_y = cv2.convertScaleAbs(src=sobel_y, alpha=0.5)
        return cv2.add(src1=sobel_x, src2=sobel_y) * amp

# ラプラシアンフィルタ
@ProcessingRegistry.register(SpatialProcessingTypes.LAPLACIAN_FILTER)
class LaplacianEdgeDetector(SpatialProcessingInterface):
    def __init__(self, requires_grayscale: bool = True):
        self.requires_grayscale = requires_grayscale

    def apply(self, gray_image: np.ndarray, kernel_size=3, amp=3):
        return cv2.convertScaleAbs(cv2.Laplacian(src=gray_image, ddepth=cv2.CV_8U, ksize=kernel_size)) * amp