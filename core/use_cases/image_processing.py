from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository

class ImageProcessingUseCase:
    def __init__(self, repository: ImageRepository):
        self.repository = repository

    def process_image(self, image_data: ImageData) -> ImageData:
        # ノイズ除去や二値化などの処理を行う
        # ここでは単純にデータを変更せずに返す
        return image_data
