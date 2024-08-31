from core.entities.image_data import ImageData
import cv2
import numpy as np

class AverageHoleDiameterCalculationUseCase:
    def calculate_average_hole_diameter(self, image_data: ImageData) -> float:
        # 画像を二値化
        gray_image = cv2.cvtColor(image_data.get_data(), cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

        # 輪郭を検出
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 各穴の直径を計算
        diameters = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 0:
                diameter = np.sqrt(4 * area / np.pi)
                diameters.append(diameter)

        # 平均直径を計算
        if diameters:
            average_diameter = sum(diameters) / len(diameters)
        else:
            average_diameter = 0

        return average_diameter
