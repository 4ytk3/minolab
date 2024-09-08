from domain.entities.image_data import ImageData
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

import cv2
import numpy as np

# 画像を読み込み（グレースケール）
image = cv2.imread('22.jpg', cv2.IMREAD_GRAYSCALE)  # 22.jpgのところに画像のファイル名を入れてください

# ガウシアンフィルタでノイズを除去
blurred_image = cv2.GaussianBlur(image, (5, 5), 1.4)

# 二値化するための閾値を設定
threshold_value = 178   # 閾値は各自で設定してください

# 画像を二値化する
_, binary_image = cv2.threshold(blurred_image, threshold_value, 255, cv2.THRESH_BINARY)

# 二値化した画像にラベリングを適用する
num_labels, labeled_image = cv2.connectedComponents(binary_image)

# 各ラベルの面積を計算する
label_areas = []
resolution = 0.083692  # 分解能（ピクセルサイズ）

for label in range(1, num_labels):  # 背景（ラベル0）を除く各ラベルについて
    pixel_area = np.sum(labeled_image == label)
    physical_area = (resolution ** 2) * pixel_area
    label_areas.append((label, physical_area))

# 各ラベルの面積を出力
for label, area in label_areas:
    print(f"Label {label}: area = {area}")

# ラベル付け後の領域を確認（面積が大きい順に上位3つのラベルを表示）
for idx, (label, area) in enumerate(sorted(label_areas, key=lambda x: x[1], reverse=True)[:3]): #[:3]の3の部分を変更すると上位〇つのラベルの表示に変更可能
    img_labeled = cv2.compare(labeled_image, label, cv2.CMP_EQ)
    cv2.namedWindow(f'Label {label}', cv2.WINDOW_NORMAL)    # ここ無くても可
    cv2.imshow(f'Label {label}', img_labeled)
    cv2.waitKey(0)

# 面積から直径を計算し、誤差を含む結果を出力
diameters = []

for label, area in label_areas:
    diameter = 2 * np.sqrt(area / np.pi)  # 直径を計算
    if diameter >= 2:   # 直径が2μm以上の穴のみ平均にカウント。必要に応じて直径を変更可能
        diameters.append(diameter)
        print(f"Label {label}: Diameter = {diameter}")  # ラベル毎の直径を出力

if diameters:
    average_diameter = np.mean(diameters)
    std_deviation = np.std(diameters)
    print(f"穴の数: {len(diameters)}, 粒子径平均: {average_diameter} ± {std_deviation}")
else:
    print("穴の数: 0")

# 二値化した画像を表示する
cv2.namedWindow('Binary Image', cv2.WINDOW_NORMAL)
cv2.imshow('Binary Image', binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()