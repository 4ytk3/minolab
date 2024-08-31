import flet as ft
from domain.use_cases.average_hole_diameter_calculation import AverageHoleDiameterCalculationUseCase
from infrastructure.repositories.file_image_repository import FileImageRepository
from PIL import Image

def main(page: ft.Page):
    page.title = "Average Hole Diameter Calculation"
    page.window_width = 600
    page.window_height = 400

    repository = FileImageRepository()
    hole_diameter_use_case = AverageHoleDiameterCalculationUseCase()

    image_display = ft.Image(src="", width=300, height=300, fit=ft.ImageFit.CONTAIN)
    image_data = None

    def on_open_files_result(e: ft.FilePickerResultEvent):
        nonlocal image_data
        if e.files:
            file_path = e.files[0].path
            image_data = repository.load_from_file(file_path)
            img = Image.fromarray(image_data.get_data())
            img.show()
            image_display.src = file_path
            image_display.update()

            average_diameter = hole_diameter_use_case.calculate_average_hole_diameter(image_data)
            page.snack_bar = ft.SnackBar(ft.Text(f"Average Hole Diameter: {average_diameter:.2f} pixels"))
            page.snack_bar.open = True
            page.update()

    def on_save_files_result(e: ft.FilePickerResultEvent):
        if e.path and image_data:
            try:
                # 画像を元のフォーマットで保存
                repository.save_to_file(image_data, e.path)
                page.snack_bar = ft.SnackBar(ft.Text(f"Image saved as {e.path}"))
                page.snack_bar.open = True
                page.update()
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Failed to save image: {str(ex)}"))
                page.snack_bar.open = True
                page.update()

    def save_image(e):
        save_file_picker.save_file(file_types=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])

    open_file_picker = ft.FilePicker(on_result=on_open_files_result)
    save_file_picker = ft.FilePicker(on_result=on_save_files_result)
    page.overlay.append(open_file_picker)
    page.overlay.append(save_file_picker)

    select_button = ft.ElevatedButton(text="Select Image", on_click=lambda e: open_file_picker.pick_files(allow_multiple=False))
    save_button = ft.ElevatedButton(text="Save Image As...", on_click=save_image)

    page.add(select_button, save_button, image_display)

if __name__ == "__main__":
    ft.app(target=main)
