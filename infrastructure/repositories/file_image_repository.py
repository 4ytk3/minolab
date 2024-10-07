import cv2
import dm3_lib
import dm4
from domain.entities.image_data import ImageData
from domain.repositories.image_repository_interface import ImageRepositoryInterface

class FileImageRepository(ImageRepositoryInterface):
    def load_image(self, file_path: str) -> ImageData:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ValueError(f"Failed to load image from {file_path}")
            return ImageData(image=image, format=file_path.split('.')[-1], space='rgb')
        
        elif file_path.lower().endswith('.dm3'):
            image = load_dm3(file_path)
            return ImageData(image=image, format='dm3', space='grayscale')
        
        elif file_path.lower().endswith('.dm4'):
            image = load_dm4(file_path)
            return ImageData(image=image, format='dm4', space='grayscale')
        
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    def save_image(self, image_data: ImageData, file_path: str) -> None:
        format_extension = image_data.get_format()
        if format_extension in ['jpg', 'jpeg', 'png', 'bmp']:
            success = cv2.imwrite(file_path, image_data.get_image())
            if not success:
                raise ValueError(f"Failed to save image to {file_path}")
        else:
            raise ValueError(f"Saving in format {format_extension} is not supported")