from typing import Tuple
from domain.entities.image_data import ImageData
from domain.config.processing_types import SpatialProcessingTypes, FrequencyProcessingTypes
from domain.services.processing_registry import SpatialProcessingRegistry, FrequencyProcessingRegistry

class SpatialProcessing:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def spatial_processing(self, image_data: ImageData, **kwargs) -> ImageData:
        if not SpatialProcessingTypes[self.processing_type]:
            raise ValueError(f"Unsupported processing type: {self.processing_type}")

        processing_cls = SpatialProcessingRegistry.get_processing(self.processing_type)





        return processing_cls.apply(image_data)

class FrequencyImageProcessor:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def frequency_processing(self, image_data: ImageData, **kwargs) -> Tuple[ImageData, ImageData]:
        if FrequencyProcessingTypes[self.processing_type]:
            processing_cls = FrequencyProcessingRegistry.get_processing(self.processing_type)
            return processing_cls.apply(image_data)
        else:
            raise ValueError(f"Unsupported processing type: {self.processing_type}")