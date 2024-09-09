from domain.entities.image_data import ImageData
from domain.config.processing_types import SpatialProcessingTypes, FrequencyProcessingTypes
from domain.services.spatial_processing import spatial_filters, binarizations, edge_detectors
from domain.services.frequency_processing import frequency_filters, peak_detector
from domain.use_cases.image_processing import SpatialProcessing, FrequencyProcessing
from domain.use_cases.crystal_detection import CrystalDetector
#from domain.use_cases.average_hole_diameter_calculation import AverageHoleDiameterCalculationUseCase
#from domain.use_cases.tomography import TomographyUseCase

import flet as ft
import os
import cv2

def main(page: ft.Page):
    page.title = "minolab"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200
    page.window.height = 800
    page.window.resizable = True
    current_function = ft.Text("Image Processing", size=24, weight=ft.FontWeight.BOLD)

    def change_tab(e):
        selected_index = e.control.selected_index
        nav_rail.selected_index = selected_index
        current_function.value = nav_rail.destinations[selected_index].label
        for i, content in enumerate(tab_contents):
            content.visible = (i == selected_index)
        page.update()

    def toggle_nav_rail(e):
        nav_rail.visible = not nav_rail.visible
        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.IMAGE, selected_icon=ft.icons.FILTER, label="Image Processing"),
            ft.NavigationRailDestination(icon=ft.icons.AUTO_AWESOME, selected_icon=ft.icons.AUTO_AWESOME, label="Fourier Transform"),
            ft.NavigationRailDestination(icon=ft.icons.AUTO_FIX_HIGH, selected_icon=ft.icons.AUTO_FIX_HIGH, label="Crystal Detector"),
            ft.NavigationRailDestination(icon=ft.icons.CIRCLE, selected_icon=ft.icons.CIRCLE, label="Calc Average Diameter"),
            ft.NavigationRailDestination(icon=ft.icons.VIEW_IN_AR, selected_icon=ft.icons.VIEW_IN_AR, label="Tomography"),
        ],
        on_change=change_tab,
    )

    selected_images = []
    current_image_index = 0
    original_image = None

    def on_images_select(e: ft.FilePickerResultEvent):
        nonlocal selected_images, current_image_index, original_image
        if e.files:
            if selected_images:
                show_save_confirmation_dialog()
            else:
                process_selected_files(e.files)

    def process_selected_files(files):
        nonlocal selected_images, current_image_index, original_image
        selected_images = [(f.name, f.path) for f in files]
        current_image_index = 0
        if selected_images:
            original_image = ft.Image(src=selected_images[0][1])
        update_preview()

    def on_folder_select(e: ft.FilePickerResultEvent):
        nonlocal selected_images, current_image_index, original_image
        if e.path:
            if selected_images:
                show_save_confirmation_dialog(folder_path=e.path)
            else:
                process_selected_folder(e.path)

    def process_selected_folder(folder_path):
        nonlocal selected_images, current_image_index, original_image
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        selected_images = [(f, os.path.join(folder_path, f)) for f in os.listdir(folder_path) if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(folder_path, f))]
        current_image_index = 0
        if selected_images:
            original_image = ft.Image(src=selected_images[0][1])
        update_preview()

    def update_preview():
        if selected_images:
            preview_image.src = selected_images[current_image_index][1]
            preview_image.visible = True
            image_name.value = f"Current image: {selected_images[current_image_index][0]}"
            left_arrow.visible = current_image_index > 0
            right_arrow.visible = current_image_index < len(selected_images) - 1
            left_spacer.visible = not left_arrow.visible
            right_spacer.visible = not right_arrow.visible
        else:
            preview_image.visible = False
            image_name.value = ""
            left_arrow.visible = False
            right_arrow.visible = False
            left_spacer.visible = True
            right_spacer.visible = True
        page.update()

    def navigate_image(direction):
        nonlocal current_image_index
        current_image_index += direction
        update_preview()

    file_picker = ft.FilePicker(on_result=on_images_select)
    folder_picker = ft.FilePicker(on_result=on_folder_select)
    page.overlay.extend([file_picker, folder_picker])

    def save_image(e):
        if preview_image.visible:
            save_path = ft.FilePicker()
            save_path.save_file(file_name="processed_image.png", allowed_extensions=["png", "jpg", "jpeg"])
            page.overlay.append(save_path)
            page.update()

    def save_all_images(e):
        if selected_images:
            save_path = ft.FilePicker()
            save_path.get_directory_path()
            page.overlay.append(save_path)
            page.update()

    select_images_button = ft.ElevatedButton("Select Images", icon=ft.icons.PHOTO_LIBRARY, on_click=lambda _: file_picker.pick_files(allow_multiple=True))
    select_folder_button = ft.ElevatedButton("Select Folder", icon=ft.icons.FOLDER, on_click=lambda _: folder_picker.get_directory_path())

    preview_image = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=400, height=400)
    image_name = ft.Text("", size=14)

    left_arrow = ft.IconButton(ft.icons.ARROW_BACK_IOS_NEW, visible=False, on_click=lambda _: navigate_image(-1))
    right_arrow = ft.IconButton(ft.icons.ARROW_FORWARD_IOS, visible=False, on_click=lambda _: navigate_image(1))
    left_spacer = ft.Container(width=50, visible=False)
    right_spacer = ft.Container(width=50, visible=False)

    undo_button = ft.IconButton(ft.icons.UNDO, on_click=lambda _: print("Undo"))
    redo_button = ft.IconButton(ft.icons.REDO, on_click=lambda _: print("Redo"))

    save_button = ft.ElevatedButton("Save", icon=ft.icons.SAVE, on_click=save_image)
    save_all_button = ft.ElevatedButton("Save All", icon=ft.icons.SAVE_ALT, on_click=save_all_images)

    slider_values = {
        "kernel_size": 5,
        "sigmaX": 1.0,
        "sigmaColor": 50,
        "sigmaSpace": 50,
        "threshold": 128,
        "min_val": 50,
        "max_val": 150,
        "radius": 50,
        "inner_radius": 30,
        "outer_radius": 80,
        "exclude_radius": 30,
        "peak_threshold": 0.8
    }

    def create_slider(min_value, max_value, divisions, label, identifier):
        return ft.Slider(min=min_value, max=max_value, value=slider_values.get(identifier, min_value), divisions=divisions, label=label, visible=False, on_change=lambda e: on_slider_change(e, identifier))

    def on_image_processing_option_change(e):
        selected_option = e.control.value
        for option in image_processing_options:
            option.visible = False
        if selected_option == "Spatial Filter":
            spatial_filter_options.visible = True
        elif selected_option == "Binarization":
            binarization_options.visible = True
        elif selected_option == "Edge Detection":
            edge_detection_options.visible = True
        elif selected_option == "Line Detection":
            line_detection_options.visible = True
        hide_all_sliders()
        page.update()

    def on_spatial_filter_option_change(e):
        selected_option = e.control.value
        hide_all_sliders()
        kernel_size_slider.visible = True
        if selected_option == "Average Filter":
            processing_type = SpatialProcessingTypes.AVERAGE_FILTER
        elif selected_option == "Median Filter":
            processing_type = SpatialProcessingTypes.MEDIAN_FILTER
        elif selected_option == "Gaussian Filter":
            processing_type = SpatialProcessingTypes.GAUSSIAN_FILTER
            gaussian_sigma_slider.visible = True
        elif selected_option == "Bilateral Filter":
            processing_type = SpatialProcessingTypes.BILATERAL_FILTER
            bilateral_sigmaColor_slider.visible = True
            bilateral_sigmaSpace_slider.visible = True
        apply_preview(processing_type)
        page.update()

    def on_binarization_option_change(e):
        selected_option = e.control.value
        hide_all_sliders()
        if selected_option == "Threshold Binarization":
            processing_type = SpatialProcessingTypes.THRESHOLD_BINARIZATION
            threshold_slider.visible = True
        elif selected_option == "Otsu Binarization":
            processing_type = SpatialProcessingTypes.OTSU_BINARIZATION
        elif selected_option == "Adaptive Binarization":
            processing_type = SpatialProcessingTypes.ADAPTIVE_BINARIZATION
            adaptive_kernel_size_slider.visible = True
        apply_preview(processing_type)
        page.update()

    def on_edge_detection_option_change(e):
        selected_option = e.control.value
        hide_all_sliders()
        if selected_option == "Canny Edge Detector":
            processing_type = SpatialProcessingTypes.CANNY_EDGE_DETECTOR
            canny_low_threshold_slider.visible = True
            canny_high_threshold_slider.visible = True
        elif selected_option == "Prewitt Filter":
            processing_type = SpatialProcessingTypes.PREWITT_FILTER
            prewitt_kernel_size_slider.visible = True
        elif selected_option == "Sobel Filter":
            processing_type = SpatialProcessingTypes.SOBEL_FILTER
            edge_kernel_size_slider.visible = True
        elif selected_option == "Laplacian Filter":
            processing_type = SpatialProcessingTypes.SOBEL_FILTER
            edge_kernel_size_slider.visible = True
        apply_preview(processing_type)
        page.update()

    def hide_all_sliders():
        for slider in all_sliders:
            slider.visible = False

    def on_slider_change(e, identifier):
        slider_values[identifier] = e.control.value
        apply_preview()

    def apply_preview(processing_type: str):
        image_data = ImageData(cv2.imread(preview_image.src))
        processor = SpatialProcessing(processing_type)
        processed_image_data = processor.process(image_data, **slider_values)
        temp_image_path = save_image_to_temp(processed_image_data)
        preview_image.src = temp_image_path
        page.update()

    def on_execute_button_click(e):
        page.update()

    def save_image_to_temp(image_data: ImageData) -> str:
        temp_image_path = "temp_processed_image.jpg"
        cv2.imwrite(temp_image_path, image_data.get_image())
        return temp_image_path

    image_processing_dropdown = ft.Dropdown(
        label="Select Processing",
        options=[
            ft.dropdown.Option("Spatial Filter"),
            ft.dropdown.Option("Binarization"),
            ft.dropdown.Option("Edge Detection"),
            ft.dropdown.Option("Line Detection"),
        ],
        on_change=on_image_processing_option_change,
    )

    spatial_filter_options = ft.Dropdown(
        label="Spatial Filter",
        options=[
            ft.dropdown.Option("Average Filter"),
            ft.dropdown.Option("Median Filter"),
            ft.dropdown.Option("Gaussian Filter"),
            ft.dropdown.Option("Bilateral Filter"),
        ],
        on_change=on_spatial_filter_option_change,
        visible=False,
    )

    kernel_size_slider = create_slider(3, 15, 6, "Kernel Size", "kernel_size")
    gaussian_sigma_slider = create_slider(0, 10, 100, "Gaussian Sigma", "sigmaX")
    bilateral_sigmaColor_slider = create_slider(1, 100, 99, "Bilateral Sigmas", "sigmaColor")
    bilateral_sigmaSpace_slider = create_slider(1, 100, 99, "Bilateral Sigmas", "sigmaSpace")

    binarization_options = ft.Dropdown(
        label="Binarization Method",
        options=[
            ft.dropdown.Option("Threshold Binarization"),
            ft.dropdown.Option("Otsu Binarization"),
            ft.dropdown.Option("Adaptive Binarization"),
        ],
        on_change=on_binarization_option_change,
        visible=False,
    )

    threshold_slider = create_slider(0, 255, 255, "Threshold", "threshold")
    adaptive_kernel_size_slider = create_slider(3, 15, 6, "Adaptive Kernel Size", "kernel_size")

    edge_detection_options = ft.Dropdown(
        label="Edge Detection Method",
        options=[
            ft.dropdown.Option("Canny Edge Detector"),
            ft.dropdown.Option("Prewitt Filter"),
            ft.dropdown.Option("Sobel Filter"),
            ft.dropdown.Option("Laplacian Filter"),
        ],
        on_change=on_edge_detection_option_change,
        visible=False,
    )

    canny_low_threshold_slider = create_slider(0, 255, 255, "Canny Low Threshold", "min_val")
    canny_high_threshold_slider = create_slider(0, 255, 255, "Canny High Threshold", "max_val")
    prewitt_kernel_size_slider = create_slider(3, 9, 3 ,"Kernel Size", "kernel_size")
    edge_kernel_size_slider = create_slider(3, 15, 6, "Kernel Size", "kernel_size")

    line_detection_options = ft.Dropdown(
        label="Line Detection Method",
        options=[
            ft.dropdown.Option("Hough Transform"),
            ft.dropdown.Option("Probabilistic Hough Transform"),
            ft.dropdown.Option("LSD"),
        ],
        visible=False,
    )

    image_processing_options = [
        spatial_filter_options,
        binarization_options,
        edge_detection_options,
        line_detection_options,
    ]

    all_sliders = [
        kernel_size_slider,
        gaussian_sigma_slider,
        bilateral_sigmaColor_slider,
        bilateral_sigmaSpace_slider,
        threshold_slider,
        adaptive_kernel_size_slider,
        canny_low_threshold_slider,
        canny_high_threshold_slider,
        prewitt_kernel_size_slider,
        edge_kernel_size_slider,
    ]

    image_processing = ft.Container(
        content=ft.Column([
            image_processing_dropdown,
            *image_processing_options,
            *all_sliders,
        ]),
        padding=20,
    )

    def on_fourier_filter_change(e):
        selected_filter = e.control.value
        hide_all_sliders()
        if selected_filter in ["Lowpass Filter", "Highpass Filter"]:
            lowpass_highpass_slider.visible = True
        elif selected_filter == "Bandpass Filter":
            bandpass_inner_slider.visible = True
            bandpass_outer_slider.visible = True
        elif selected_filter == "Peak Detector":
            peak_detector_circle_slider.visible = True
            peak_detector_order_slider.visible = True
        apply_preview()
        page.update()

    fourier_filter_dropdown = ft.Dropdown(
        label="Fourier Filter",
        options=[
            ft.dropdown.Option("Lowpass Filter"),
            ft.dropdown.Option("Highpass Filter"),
            ft.dropdown.Option("Bandpass Filter"),
            ft.dropdown.Option("Peak Detector"),
        ],
        on_change=on_fourier_filter_change,
    )

    lowpass_highpass_slider = create_slider(0, 300, 300, "Circle Size", "radius")
    bandpass_inner_slider = create_slider(0, 300, 300, "Inner Circle Size", "inner_radius")
    bandpass_outer_slider = create_slider(0, 300, 300, "Outer Circle Size", "outer_radius")
    peak_detector_circle_slider = create_slider(0, 100, 100, "Center Removal Circle Size", "exclude_radius")
    peak_detector_order_slider = create_slider(0, 1, 100, "Peak Detection Order", "peak_threshold")

    fourier_transform = ft.Container(
        content=ft.Column([
            fourier_filter_dropdown,
            lowpass_highpass_slider,
            bandpass_inner_slider,
            bandpass_outer_slider,
            peak_detector_circle_slider,
            peak_detector_order_slider,
            ft.Row([
                ft.Image(src="/placeholder.svg", width=200, height=200),
                ft.Image(src="/placeholder.svg", width=200, height=200),
            ]),
        ]),
        padding=20,
    )

    calc_average_diameter = ft.Container(
        content=ft.Text("Calc Average Diameter content goes here"),
        padding=20,
    )

    custom_processing = ft.Container(
        content=ft.Column([
            ft.Text("Custom Processing", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Image(src="/placeholder.svg", width=200, height=200),
                ft.Image(src="/placeholder.svg", width=200, height=200),
            ]),
            ft.Row([
                ft.Image(src="/placeholder.svg", width=200, height=200),
                ft.Image(src="/placeholder.svg", width=200, height=200),
            ]),
            ft.Text("Pixel count results will be displayed here"),
        ]),
        padding=20,
    )

    tomography = ft.Container(
        content=ft.Text("Tomography content goes here"),
        padding=20,
    )

    tab_contents = [
        image_processing,
        fourier_transform,
        calc_average_diameter,
        custom_processing,
        tomography,
    ]

    for i, content in enumerate(tab_contents):
        content.visible = (i == 0)

    execute_button = ft.ElevatedButton("Execute", on_click=on_execute_button_click)

    def show_save_confirmation_dialog(folder_path=None):
        def save_and_continue(e):
            save_image(e)
            if folder_path:
                process_selected_folder(folder_path)
            else:
                process_selected_files(file_picker.result.files)
            dialog.open = False
            page.update()

        def discard_and_continue(e):
            if folder_path:
                process_selected_folder(folder_path)
            else:
                process_selected_files(file_picker.result.files)
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Save changes?"),
            content=ft.Text("Do you want to save the changes to the current image?"),
            actions=[
                ft.TextButton("Save", on_click=save_and_continue),
                ft.TextButton("Discard", on_click=discard_and_continue),
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, 'open', False)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def toggle_fullscreen(e):
        page.window.full_screen = not page.window.full_screen
        page.update()

    window_controls = ft.Row([
        ft.IconButton(ft.icons.MINIMIZE, on_click=lambda _: setattr(page.window, 'minimized', True)),
        ft.IconButton(ft.icons.FULLSCREEN, on_click=toggle_fullscreen),
        ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window.close()),
    ])

    content_area = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.icons.MENU, on_click=toggle_nav_rail),
                current_function,
                ft.Container(expand=True),
                window_controls,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Container(expand=True),
                undo_button,
                redo_button,
                select_images_button,
                select_folder_button,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                left_spacer, left_arrow,
                preview_image,
                right_arrow, right_spacer,
            ], alignment=ft.MainAxisAlignment.CENTER),
            *tab_contents,
            ft.Row([
                image_name,
                ft.Container(expand=True),
                execute_button,
                save_button,
                save_all_button,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]),
        padding=20,
        expand=True,
    )

    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                content_area,
            ],
            expand=True,
        )
    )

ft.app(target=main)