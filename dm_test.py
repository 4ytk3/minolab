import dm3_lib as dm3
import dm4
import glob
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

source_dir = '/home/nakasone/ghq/github.com/4ytk3/minolab/deg'
save_dir = '/home/nakasone/ghq/github.com/4ytk3/minolab/save'

filepath = glob.glob(os.path.join(source_dir, f'*.dm3'))
os.makedirs(save_dir, exist_ok=True)

pixels = 1024
dpi = 100
figsize = (pixels / dpi, pixels / dpi)

for file in filepath:
    dm3f = dm3.DM3(file)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.matshow(dm3f.imagedata, vmin=dm3f.cuts[0], vmax=dm3f.cuts[1], cmap='gray')
    base = os.path.splitext(os.path.basename(file))[0]
    ax.set_axis_off()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.savefig(save_dir + '/' + base + ".tif")
    plt.close(fig)

# dm3
# dm3f = dm3.DM3("0.dm3")
# # print some useful image information
# print(dm3f.info)
# # print("pixel size = %s %s"%dm3f.pxsize)
# plt.matshow(dm3f.imagedata, vmin=dm3f.cuts[0], vmax=dm3f.cuts[1], cmap='gray')
# plt.show()


# dm4
# with dm4.DM4File.open("test_images/17_800k.dm4") as dm4data:
#     # ディレクトリを読み込む
#     tags = dm4data.read_directory()

#     # 'ImageList'から画像データを取り出す
#     image_data_tag = tags.named_subdirs['ImageList'].unnamed_subdirs[1].named_subdirs['ImageData']
#     image_tag = image_data_tag.named_tags['Data']

#     # 画像のサイズを取得
#     XDim = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[0])
#     YDim = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[1])

#     # 画像データを読み込み、numpy配列に変換
#     np_array = np.array(dm4data.read_tag_data(image_tag), dtype=np.uint16)
#     np_array = np.reshape(np_array, (YDim, XDim))

#     # 画像を表示する
#     plt.imshow(np_array, cmap='gray')  # グレースケールで表示
#     plt.title("DM4 Image")
#     plt.axis('off')
#     plt.show()
