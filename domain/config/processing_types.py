from enum import Enum

class SpatialProcessingTypes(Enum):
    # ノイズ処理
    AVERAGE_FILTER = "Average Filter"
    MEDIAN_FILTER = "Median Filter"
    GAUSSIAN_FILTER = "Gaussian Filter"
    BILATERAL_FILTER = "Bilateral Filter"

    # 二値化
    THRESHOLD_BINARIZATION = "Threshold Binarization"
    OTSU_BINARIZATION = "Otsu Binarization"
    ADAPTIVE_BINARIZATION = "Adaptive Binarization"

    # エッジ抽出
    CANNY_EDGE_DETECTOR = "Canny Edge Detector"
    PREWITT_FILTER = "Prewitt Filter"
    SOBEL_FILTER = "Sobel Filter"
    LAPLACIAN_FILTER = "Laplacian Filter"

    # 他のフィルタや処理タイプがあればここに追加
    # 例: CUSTOM_FILTER = "Custom Filter"

class FrequencyProcessingTypes(Enum):
    # ノイズ処理
    LOWPASS_FILTER = "Lowpass Filter"
    HIGHPASS_FILTER = "Highpass Filter"
    BANDPASS_FILTER = "Bandpass Filter"

    # ピーク検出
    PEAK_DETECTOR = "Peak Detector"