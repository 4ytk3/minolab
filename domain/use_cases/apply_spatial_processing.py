from domain.entities.image_data import ImageData
from domain.services.processing_registry import ProcessingRegistry
from domain.services.image_processing_helpers import convert_to_grayscale

class ApplySpatialProcessing:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def apply_processing(self, image_data: ImageData, **kwargs) -> ImageData:
        processing_cls = ProcessingRegistry.get_processing(self.processing_type)
        if processing_cls.requires_grayscale and image_data.get_color_space() != "grayscale":
            image_data = convert_to_grayscale(image_data)
        processed_image = processing_cls.apply(image_data.get_data(), **kwargs)
        return ImageData(data=processed_image, format=image_data.get_format(), color_space=image_data.get_color_space())
