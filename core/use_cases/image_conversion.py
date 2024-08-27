from core.repositories.image_repository import ImageRepository

class ImageConversionUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def convert_format(self, input_path: str, output_path: str, output_format: str):
        image_data = self.image_repository.load(input_path)
        self.image_repository.save(image_data, output_path, output_format)
