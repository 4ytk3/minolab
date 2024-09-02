from domain.entities.image_data import ImageData
from domain.services.processing_registry import ProcessingRegistry
from domain.services.image_processing_helpers import convert_to_grayscale

class ApplyFrequencyProcessing:
    def __init__(self, processing_type: str):
        self.processing_type = processing_type

    def apply_processing(self, image_data: ImageData, **kwargs) -> list[ImageData, ImageData]:
        processing_cls = ProcessingRegistry.get_processing(self.processing_type)
        if processing_cls.requires_grayscale and image_data.get_color_space() != "grayscale":
            image_data = convert_to_grayscale(image_data)
        fft_image, ifft_image = processing_cls.apply(image_data.get_data(), **kwargs)
        fft_data = ImageData(data=fft_image, format=image_data.get_format(), color_space=image_data.get_color_space())
        ifft_data = ImageData(data=ifft_image, format=image_data.get_format(), color_space=image_data.get_color_space())
        return fft_data, ifft_data
