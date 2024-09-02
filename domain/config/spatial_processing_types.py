class SpatialProcessingTypes:
    # 二値化
    THRESHOLD_BINARIZATION = 'threshold_binarization'
    OTSU_BINARIZATION = 'otsu_binarization'
    ADAPTIVE_BINARIZATION = 'adaptive_binarization'

    # ノイズ処理
    AVERAGE_FILTER = 'average_filter'
    MEDIAN_FILTER = 'median_filter'
    GAUSSIAN_FILTER = 'gaussian_filter'
    BILATERAL_FILTER = 'bilateral_filter'

    # エッジ抽出
    CANNY_EDGE_DETECTOR = 'canny_edge_detector'
    PREWITT_FILTER = 'prewitt_filter'
    SOBELFILTER = 'sobel_filter'
    LAPLACIAN_FILTER = 'laplacian_filter'

    # 他のフィルタや処理タイプがあればここに追加
    # 例: CUSTOM_FILTER = 'custom_filter'