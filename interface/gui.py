import flet as ft
from core.use_cases.image_conversion import ImageConversionUseCase
from core.use_cases.image_processing import ImageProcessingUseCase
from infrastructure.repositories.file_image_repository import FileImageRepository

def main(page: ft.Page):
    def convert_image(e):
        input_path = input_path_field.value
        output_path = output_path_field.value
        output_format = output_format_field.value
        
        repository = FileImageRepository()
        use_case = ImageConversionUseCase(repository)
        use_case.convert_format(input_path, output_path, output_format)

        result_label.value = "Conversion Successful!"
        result_label.update()

    def process_image(e):
        input_path = input_path_field.value
        output_path = output_path_field.value
        
        repository = FileImageRepository()
        use_case = ImageProcessingUseCase(repository)
        use_case.process_image(input_path, output_path)

        result_label.value = "Processing Successful!"
        result_label.update()

    input_path_field = ft.TextField(label="Input Image Path")
    output_path_field = ft.TextField(label="Output Image Path")
    output_format_field = ft.TextField(label="Output Format")
    convert_button = ft.Button(text="Convert", on_click=convert_image)
    process_button = ft.Button(text="Process", on_click=process_image)
    result_label = ft.Text()

    page.add(input_path_field, output_path_field, output_format_field, convert_button, process_button, result_label)

if __name__ == "__main__":
    ft.app(target=main)
