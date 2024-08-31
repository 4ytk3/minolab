from domain.entities.image_data import ImageData
from typing import List

class TomographyUseCase:
    def perform_tomography(self, images: List[ImageData]) -> ImageData:
        # 複数の画像からトモグラフィー処理を実行
        return images[0]  # 仮の処理
