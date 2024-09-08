from typing import Tuple
from domain.entities.image_data import ImageData
from domain.services.processing_registry import SpatialProcessingRegistry, FrequencyProcessingRegistry
from domain.utilities.image_converters import rgb2gray

class BaseProcessing:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def _ensure_grayscale(self, image_data: ImageData, processing_cls):
        if processing_cls.REQUIRES_GRAYSCALE and image_data.get_space() != "grayscale":
            image_data = rgb2gray(image_data)
        return image_data

class SpatialProcessing(BaseProcessing):
    def process(self, image_data: ImageData, **kwargs) -> ImageData:
        processing_cls = SpatialProcessingRegistry.get_processing(self.processing_type)
        image_data = self._ensure_grayscale(image_data, processing_cls)
        processed_image = processing_cls.apply(image_data.get_image(), **kwargs)

        return ImageData(
            image=processed_image,
            format=image_data.get_format(),
            space=image_data.get_space()
        )

class FrequencyProcessing(BaseProcessing):
    def process(self, image_data: ImageData, **kwargs) -> Tuple[ImageData, ImageData]:
        processing_cls = FrequencyProcessingRegistry.get_processing(self.processing_type)
        image_data = self._ensure_grayscale(image_data, processing_cls)
        fft_image, ifft_image = processing_cls.apply(image_data.get_image(), **kwargs)

        return (
            ImageData(
                image=fft_image,
                format=image_data.get_format(),
                space="frequency"
            ),
            ImageData(
                image=ifft_image,
                format=image_data.get_format(),
                space=image_data.get_space()
            )
        )