import cv2
import numpy as np
from domain.config.processing_types import SpatialProcessingTypes
from domain.services.processing_registry import SpatialProcessingRegistry
from domain.services.spatial_processing.spatial_processing_interface import SpatialProcessingInterface

# Cannyエッジ検出器
@SpatialProcessingRegistry.register(SpatialProcessingTypes.CANNY_EDGE_DETECTOR)
class CannyEdgeDetector(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, min_val: int = 100, max_val: int = 300) -> np.ndarray:
        return cv2.Canny(image=gray_image, threshold1=min_val, threshold2=max_val, L2gradient=False)

# プレヴィットフィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.PREWITT_FILTER)
class PrewittFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, kernel_size: int = 3, **kwargs) -> np.ndarray:
        prewitt_x, prewitt_y = self.make_kernel(kernel_size)
        edge_x = cv2.filter2D(gray_image, -1, prewitt_x)
        edge_y = cv2.filter2D(gray_image, -1, prewitt_y)
        return np.sqrt(edge_x**2 + edge_y**2)

    def make_kernel(self, kernel_size: int = 3):
        assert kernel_size in [3, 5, 7], f"kernel_size={kernel_size} is not supported"
        if kernel_size == 3:
            return np.array([[1,1,1],[0,0,0],[-1,-1,-1]]), np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        elif kernel_size == 5:
            return (np.array([[2,2,2,2,2],[1,1,1,1,1],[0,0,0,0,0],[-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2]]),
                    np.array([[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2],[-2,-1,0,1,2]]))
        elif kernel_size == 7:
            return (np.array([[3,3,3,3,3,3,3],[2,2,2,2,2,2,2],[1,1,1,1,1,1,1],[0,0,0,0,0,0,0],[-1,-1,-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2,-2,-2],[-3,-3,-3,-3,-3,-3,-3]]),
                    np.array([[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3],[-3,-2,-1,0,1,2,3]]))

# ソーベルフィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.SOBEL_FILTER)
class SobelFilter(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, dx=1, dy=1, kernel_size=3, amp=3, **kwargs) -> np.ndarray:
        edge_x = cv2.Sobel(src=gray_image, ddepth=cv2.CV_8U, dx=dx, dy=dy, ksize=kernel_size) # X方向
        edge_y = cv2.Sobel(src=gray_image, ddepth=cv2.CV_8U, dx=dx, dy=dy, ksize=kernel_size) # Y方向
        edge_x = cv2.convertScaleAbs(src=edge_x, alpha=0.5)
        edge_y = cv2.convertScaleAbs(src=edge_y, alpha=0.5)
        return cv2.add(src1=edge_x, src2=edge_y) * amp

# ラプラシアンフィルタ
@SpatialProcessingRegistry.register(SpatialProcessingTypes.LAPLACIAN_FILTER)
class LaplacianEdgeDetector(SpatialProcessingInterface):
    REQUIRES_GRAYSCALE = True

    def apply(self, gray_image: np.ndarray, kernel_size=3, amp=3, **kwargs) -> np.ndarray:
        return cv2.convertScaleAbs(cv2.Laplacian(src=gray_image, ddepth=cv2.CV_8U, ksize=kernel_size)) * amp