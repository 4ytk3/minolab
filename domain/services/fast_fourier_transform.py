import numpy as np
from domain.entities.image_data import ImageData
from domain.services.filters.spatial_filter_interface import FilterInterface

class FFTFilter(FilterInterface):
    def apply(self, image_data: ImageData) -> ImageData:
        gray_image = image_data.get_data()  # 画像データを取得
        fshift = np.fft.fftshift(np.fft.fft2(gray_image))  # 2次元フーリエ変換とシフト
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)  # スペクトルの振幅
        return ImageData(data=magnitude_spectrum.astype(np.float32), format=image_data.get_format(), color_space=image_data.get_color_space())

class IFFTFilter(FilterInterface):
    def apply(self, image_data: ImageData) -> ImageData:
        f_ishift = np.fft.ifftshift(image_data.get_data())  # シフトを元に戻す
        img_back = np.abs(np.fft.ifft2(f_ishift))  # 逆フーリエ変換
        return ImageData(data=img_back.astype(np.float32), format=image_data.get_format(), color_space=image_data.get_color_space())
