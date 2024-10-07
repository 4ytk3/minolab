import dm3_lib as dm3
import dm4
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# parse DM3 file
dm3f = dm3.DM3("test_images/800k_3.dm3")
# print some useful image information
print(dm3f.info)
print("pixel size = %s %s"%dm3f.pxsize)
# display image
# plt.ion()
plt.matshow(dm3f.imagedata, vmin=dm3f.cuts[0], vmax=dm3f.cuts[1])
plt.colorbar(shrink=.8)
plt.show()

with dm4.DM4File.open("test_images/17_800k.dm4") as dm4data:
    # ディレクトリを読み込む
    tags = dm4data.read_directory()

    # 'ImageList'から画像データを取り出す
    image_data_tag = tags.named_subdirs['ImageList'].unnamed_subdirs[1].named_subdirs['ImageData']
    image_tag = image_data_tag.named_tags['Data']

    # 画像のサイズを取得
    XDim = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[0])
    YDim = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[1])

    # 画像データを読み込み、numpy配列に変換
    np_array = np.array(dm4data.read_tag_data(image_tag), dtype=np.uint16)
    np_array = np.reshape(np_array, (YDim, XDim))

    # 画像を表示する
    plt.imshow(np_array, cmap='gray')  # グレースケールで表示
    plt.title("DM4 Image")
    plt.axis('off')
    plt.show()
