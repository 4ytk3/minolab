import flet as ft
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64

def main(page: ft.Page):
    page.title = "画像処理アプリ"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    def encode_image(img):
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def on_upload(e: ft.FilePickerResultEvent):
        if e.files:
            global original_image
            original_image = Image.open(e.files[0].path)
            encoded_image = encode_image(original_image)
            image_view.src = f"data:image/png;base64,{encoded_image}"
            image_view.visible = True
            controls_column.visible = True
            page.update()

    def apply_filter(e):
        if not original_image:
            return

        img = original_image.copy()

        # フィルター適用
        if filter_dropdown.value == "グレースケール":
            img = img.convert('L').convert('RGB')
        elif filter_dropdown.value == "セピア":
            sepia = lambda x: tuple(int(x[0] * 0.393 + x[1] * 0.769 + x[2] * 0.189) for _ in range(3))
            img = img.convert('RGB', matrix=sepia)
        elif filter_dropdown.value == "ぼかし":
            img = img.filter(ImageFilter.BLUR)

        # 明るさ調整
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness_slider.value / 100)

        encoded_image = encode_image(img)
        processed_image_view.src = f"data:image/png;base64,{encoded_image}"
        processed_image_view.visible = True
        download_button.visible = True
        page.update()

    def save_image(e):
        img_data = base64.b64decode(processed_image_view.src.split(',')[1])
        save_path = ft.FilePicker()
        save_path.save_file(file_name="processed_image.png", allowed_extensions=["png"])
        page.overlay.append(save_path)
        page.update()

    file_picker = ft.FilePicker(on_result=on_upload)
    page.overlay.append(file_picker)

    upload_button = ft.ElevatedButton("画像をアップロード", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files())

    image_view = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=300, height=300)

    filter_dropdown = ft.Dropdown(
        label="フィルター",
        options=[
            ft.dropdown.Option("なし"),
            ft.dropdown.Option("グレースケール"),
            ft.dropdown.Option("セピア"),
            ft.dropdown.Option("ぼかし"),
        ],
        value="なし",
        width=200,
    )

    brightness_slider = ft.Slider(min=0, max=200, value=100, label="明るさ: {value}%")

    apply_button = ft.ElevatedButton("適用", on_click=apply_filter)

    processed_image_view = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=300, height=300)

    download_button = ft.ElevatedButton("ダウンロード", icon=ft.icons.DOWNLOAD, on_click=save_image, visible=False)

    controls_column = ft.Column([
        filter_dropdown,
        brightness_slider,
        apply_button
    ], visible=False)

    page.add(
        ft.Column([
            upload_button,
            image_view,
            controls_column,
            processed_image_view,
            download_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)