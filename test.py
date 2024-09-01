from domain.config.category_types import CategoryTypes
from domain.use_cases.apply_spatial_processing import ApplySpatialProcessing
from domain.entities.image_data import ImageData
import domain.services.spatial_processing.binarizations
import domain.services.spatial_processing.spatial_filters
import domain.services.spatial_processing.edge_detectors

import cv2

# 画像を読み込み、ImageDataオブジェクトとして準備
image_path = "test_images/nacl_01.jpg"
image_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image_data = ImageData(data=image_array, format="jpg")

# フィルタを適用
spatial_processing = ApplySpatialProcessing(CategoryTypes.LAPLACIAN_FILTER)
processed_image_data = spatial_processing.apply_processing(image_data)

# 結果を表示
cv2.imwrite("test_image.jpg", processed_image_data.get_data())
