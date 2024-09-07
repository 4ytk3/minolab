from domain.services.spatial_processing import spatial_filters, binarizations, edge_detectors
from domain.services.frequency_processing import frequency_filters, peak_detector

from domain.config.processing_types import SpatialProcessingTypes, FrequencyProcessingTypes
from domain.use_cases.image_processing import SpatialProcessing, FrequencyProcessing
from domain.use_cases.crystal_detection import CrystalDetector
from domain.entities.image_data import ImageData

import os
import cv2

# 画像を読み込み、ImageDataオブジェクトとして準備
def load_image(path: str) -> ImageData:
    image = cv2.imread(path)
    return ImageData(image=image, format="jpg", space="rgb")

# 結果を保存
def save_image(image_data: ImageData, output_dir: str, name: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, name)
    cv2.imwrite(output_path, image_data.get_image())

# Spatialフィルタを適用し、結果を保存
def apply_and_save_spatial_filter(processing_type, image_data, output_dir, file_name):
    try:
        processing = SpatialProcessing(processing_type)
        processed_image = processing.process(image_data)
        save_image(processed_image, output_dir, file_name)
        print(f"Applied {processing_type} and saved as {file_name}")
    except Exception as e:
        print(f"Error applying {processing_type}: {str(e)}")

# Frequencyフィルタを適用し、結果を保存
def apply_and_save_frequency_filter(processing_type, image_data, output_dir, fft_file_name, ifft_file_name):
    try:
        processing = FrequencyProcessing(processing_type)
        fft_image, ifft_image = processing.process(image_data)
        save_image(fft_image, output_dir, fft_file_name)
        save_image(ifft_image, output_dir, ifft_file_name)
        print(f"Applied {processing_type} and saved FFT as {fft_file_name}, IFFT as {ifft_file_name}")
    except Exception as e:
        print(f"Error applying {processing_type}: {str(e)}")

def main():
    # 画像パスと出力ディレクトリ
    #image_path = "test_images/test.jpg"
    image_path = "test_images/nacl_01.jpg"
    output_dir = "output_images"

    # 画像を読み込み
    image_data = load_image(image_path)

    # Spatial Processing Types のテスト
    for processing_type in SpatialProcessingTypes:
        file_name = f"{processing_type.name.lower()}.jpg"
        apply_and_save_spatial_filter(processing_type, image_data, output_dir, file_name)

    # Frequency Processing Types のテスト
    for processing_type in FrequencyProcessingTypes:
        fft_file_name = f"{processing_type.name.lower()}_fft.jpg"
        ifft_file_name = f"{processing_type.name.lower()}_ifft.jpg"
        apply_and_save_frequency_filter(processing_type, image_data, output_dir, fft_file_name, ifft_file_name)

    # CrystalDetectorのテスト
    crystal_detector = CrystalDetector()
    crystal_detector.detect_crystal(image_data)

if __name__ == "__main__":
    main()
