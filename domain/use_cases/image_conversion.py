from domain.entities.image_data import ImageData
from domain.repositories.image_repository import ImageRepository

class ImageConversionUseCase:
    def __init__(self, repository: ImageRepository):
        self.repository = repository

    def convert_and_save(self, image_data: ImageData, new_format: str, file_path: str) -> None:
        # 画像フォーマットを変更する
        image_data.format = new_format
        self.repository.save_to_file(image_data, file_path)
