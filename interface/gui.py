# interfaces/gui.py

import flet as ft
from core.use_cases.image_conversion import ImageConversionUseCase
from core.use_cases.image_processing import ImageProcessingUseCase
from infrastructure.repositories.file_image_repository import FileImageRepository
from PIL import Image

def main(page: ft.Page):
    page.title = "Image Viewer"
    page.window_width = 600
    page.window_height = 400

    repository = FileImageRepository()
    conversion_use_case = ImageConversionUseCase(repository)
    processing_use_case = ImageProcessingUseCase(repository)

    image_display = ft.Image(src="", width=300, height=300, fit=ft.ImageFit.CONTAIN)

    def on_open_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            image_data = repository.load_from_file(file_path)
            img = Image.fromarray(image_data.get_data())
            img.show()
            image_display.src = file_path
            image_display.update()

    def on_save_files_result(e: ft.FilePickerResultEvent):
        if e.path:
            try:
                img = Image.open(image_display.src)
                image_data = repository.load_from_file(image_display.src)
                conversion_use_case.convert_and_save(image_data, 'PNG', e.path)
                page.snack_bar = ft.SnackBar(ft.Text(f"Image saved as {e.path}"))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Failed to save image: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

    def save_image(e):
        save_file_picker.save_file(file_types=[("PNG files", "*.png")])

    open_file_picker = ft.FilePicker(on_result=on_open_files_result)
    save_file_picker = ft.FilePicker(on_result=on_save_files_result)
    page.overlay.append(open_file_picker)
    page.overlay.append(save_file_picker)

    select_button = ft.ElevatedButton(text="Select Image", on_click=lambda e: open_file_picker.pick_files(allow_multiple=False))
    save_button = ft.ElevatedButton(text="Save Image As...", on_click=save_image)

    page.add(select_button, save_button, image_display)

if __name__ == "__main__":
    ft.app(target=main)
