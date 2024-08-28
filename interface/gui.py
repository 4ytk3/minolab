import flet as ft
from core.entities.image_data import ImageData
from infrastructure.repositories.file_image_repository import FileImageRepository
import numpy as np
from PIL import Image

def main(page: ft.Page):
    # 初期設定
    page.title = "Image Viewer"
    page.window_width = 600
    page.window_height = 400

    # リポジトリのインスタンスを作成
    repository = FileImageRepository()

    # 画像を表示するためのImageコントロール
    image_display = ft.Image(src="", width=300, height=300, fit=ft.ImageFit.CONTAIN)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            # ファイルから画像を読み込む
            image_data = repository.load_from_file(file_path)
            # PIL Imageオブジェクトに変換して表示
            img = Image.fromarray(image_data.get_data())
            img.show()  # 画像を表示するための簡易的な方法

            # GUI上の画像表示コントロールに画像を設定
            image_display.src = file_path
            image_display.update()

    def save_files_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                img = Image.open(image_display.src)
                img.save(e.path)
                page.snack_bar = ft.SnackBar(ft.Text(f"Image saved as {e.path}"))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Failed to save image: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

    # ToDo
    # can't save
    def save_image(e):
        # ファイルの保存ダイアログを表示
        file_picker.save_file(
            file_name="saved_image.png",
            file_type="image/png"
        )

    # ファイルピッカーコントロール
    file_picker = ft.FilePicker(on_result=pick_files_result)
    save_file_picker = ft.FilePicker(on_result=save_files_result)
    page.overlay.append(file_picker)
    page.overlay.append(save_file_picker)

    # ボタンとレイアウト
    select_button = ft.ElevatedButton(text="Select Image", on_click=lambda e: file_picker.pick_files(allow_multiple=False))
    save_button = ft.ElevatedButton(text="Save Image", on_click=save_image)

    # ページに要素を追加
    page.add(select_button, save_button, image_display)

if __name__ == "__main__":
    ft.app(target=main)
