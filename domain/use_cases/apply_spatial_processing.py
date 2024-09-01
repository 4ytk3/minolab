from domain.entities.image_data import ImageData
from domain.services.spatial_processing.spatial_processing_registry import SpatialProcessingRegistry

class ApplySpatialProcessing:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def apply_processing(self, image_data: ImageData, **kwargs) -> ImageData:
        processing_cls = SpatialProcessingRegistry.get_processing(self.processing_type)
        processed_image = processing_cls.apply(image_data.get_data(), **kwargs)
        return ImageData(data=processed_image, format=image_data.get_format())
