from core.entities.image_data import ImageData
from core.repositories.image_repository import ImageRepository

class ImageProcessingUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def process_image(self, input_path: str, output_path: str):
        image_data = self.image_repository.load(input_path)
        # ここで画像処理を行います。例として、データをそのまま保存します。
        processed_image_data = self.simple_process(image_data)
        self.image_repository.save(processed_image_data, output_path, "PNG")

    def simple_process(self, image_data: ImageData) -> ImageData:
        # 簡単な画像処理ロジック（ここではデータをそのまま返す）
        return image_data
