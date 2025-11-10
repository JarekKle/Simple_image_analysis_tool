from tkinter import Tk
import tkinter as tk

from PIL import ImageTk

from coordinates import Coordinates
from image_display import ImageDisplay
from image_manager import ImageManager
from image_processor import ImageProcessor


class AppWindow:
    def __init__(self, manager: ImageManager, processor: ImageProcessor, display: ImageDisplay):
        self.manager = manager
        self.display = display
        self.processor = processor
        self.master = Tk()
        self.photo = None
        self.current_pixel_rgb = (0, 0, 0)
        self.current_pixel_coords = Coordinates(0, 0)
        self.real_pixel_coords = Coordinates(0, 0)
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)
        self._setup_window()

    def zoom(self, direction):
        self.display.zoom(direction)
        self.display.calculate_image_bounds()
        self.update_window()

    def move(self, dx, dy):
        self.display.move(dx, dy)
        self.display.calculate_image_bounds()
        self.update_window()

    def update_image(self):
        img = self.display.update_image()
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.create_image(0, 0, anchor="nw", image=self.photo)

    def update_status_bar(self):
        r, g, b = self.current_pixel_rgb
        x, y = self.real_pixel_coords
        zoom = self.display.zoom_factor
        if self.manager.is_image_grayscale(self.manager.handler.img_modified):
            self.status_bar.config(
                text=f"Zoom: {zoom}x | Pozycja: ({x}, {y}) | RGB: {r}"
            )
        else:
            self.status_bar.config(
                text=f"Zoom: {zoom}x | Pozycja: ({x}, {y}) | RGB: ({r}, {g}, {b})"
            )

    def update_window(self):
        self.update_image()
        self.update_status_bar()

    def get_pixel_value(self, event):
        width, height = self.manager.handler.img_display.size
        if 0 <= event.x < width and 0 <= event.y < height:
            self.current_pixel_coords = Coordinates(event.x, event.y)
            self.calculate_real_pixel_coords()
            self.current_pixel_rgb = self.display.get_pixel_value(self.real_pixel_coords)
            self.update_status_bar()

    def calculate_real_pixel_coords(self):
        border_left = self.display.border_left
        zoom = self.display.zoom_factor
        x, y = self.current_pixel_coords
        self.real_pixel_coords = Coordinates(int(border_left.x + x // zoom), int(border_left.y + y // zoom))

    def change_pixel_color(self, event):
        self.processor.change_pixel_color(self.real_pixel_coords)
        self.update_window()

    def _setup_window(self):
        self.master.title("Image_viewer")
        self._setup_canvas()
        self._setup_status_bar()
        self._setup_controls()
        self._setup_events()

    def _setup_canvas(self):
        img = self.manager.handler.img_modified
        width, height = img.size
        self.photo = ImageTk.PhotoImage(img)
        self.image_label = tk.Canvas(self.master, width=width, height=height)
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.image_label.create_image(0, 0, anchor="nw", image=self.photo)

    def _setup_controls(self):
        controls_frame = tk.Frame(self.master)
        controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        arrow_frame = tk.Frame(controls_frame)
        arrow_frame.pack(side=tk.TOP, pady=5)

        self.button_up = tk.Button(arrow_frame, text="↑", width=12)
        self.button_up.grid(row=0, column=1)

        self.button_left = tk.Button(arrow_frame, text="←", width=6, height=3)
        self.button_left.grid(row=1, column=0, rowspan=2)

        self.button_zoom_in = tk.Button(arrow_frame, text="+ Zoom in", width=12)
        self.button_zoom_in.grid(row=1, column=1)

        self.button_zoom_out = tk.Button(arrow_frame, text="- Zoom out", width=12)
        self.button_zoom_out.grid(row=2, column=1)

        self.button_right = tk.Button(arrow_frame, text="→", width=6, height=3)
        self.button_right.grid(row=1, column=2, rowspan=2)

        self.button_down = tk.Button(arrow_frame, text="↓", width=12)
        self.button_down.grid(row=3, column=1)

        button_frame = tk.Frame(controls_frame)
        button_frame.pack(side=tk.TOP, pady=10, fill=tk.X)

        self.button_restore_original = tk.Button(button_frame, text="Restore original image", width=18)
        self.button_restore_original.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_convert_to_grayscale = tk.Button(button_frame, text="Convert to grayscale", width=18)
        self.button_convert_to_grayscale.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_adjust_brightness = tk.Button(button_frame, text="Adjust brightness", width=18)
        self.button_adjust_brightness.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_display_histogram = tk.Button(button_frame, text="Display histogram", width=18)
        self.button_display_histogram.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_stretch_histogram = tk.Button(button_frame, text="Stretch histogram", width=18)
        self.button_stretch_histogram.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_equalize_histogram = tk.Button(button_frame, text="Equalize histogram", width=18)
        self.button_equalize_histogram.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_linear_filters = tk.Button(button_frame, text="Apply linear filter", width=18)
        self.button_linear_filters.pack(side=tk.TOP, fill=tk.X, pady=2)

        self.button_median_filter = tk.Button(button_frame, text="Apply median filter", width=18)
        self.button_median_filter.pack(side=tk.TOP, fill=tk.X, pady=2)

    def _setup_status_bar(self):
        self.status_bar = tk.Label(self.master, text="Info will be displayed here", anchor="w", relief="sunken")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def _setup_events(self):
        self.image_label.bind("<Motion>", self.get_pixel_value)
        self.image_label.bind("<Button-1>", self.change_pixel_color)

        buttons = {
            self.button_up: (0, 1),
            self.button_down: (0, -1),
            self.button_left: (-1, 0),
            self.button_right: (1, 0),
        }
        for btn, direction in buttons.items():
            btn.config(command=lambda d=direction: self.move(*d))

        self.button_zoom_in.config(command=lambda: self.zoom(1))
        self.button_zoom_out.config(command=lambda: self.zoom(-1))

        self.button_restore_original.config(command=self.restore_original)
        self.button_convert_to_grayscale.config(command=self.convert_to_grayscale)
        self.button_adjust_brightness.config(command=self.adjust_brightness)
        self.button_display_histogram.config(command=self.display_histogram)
        self.button_stretch_histogram.config(command=self.stretch_histogram)
        self.button_equalize_histogram.config(command=self.equalize_histogram)
        self.button_linear_filters.config(command=self.linear_filters)
        self.button_median_filter.config(command=self.median_filter)

    def restore_original(self):
        self.manager.restore_original()
        self.update_window()

    def convert_to_grayscale(self):
        self.manager.convert_to_grayscale()
        self.update_window()

    def adjust_brightness(self):
        self.processor.adjust_brightness()
        self.update_window()

    def display_histogram(self):
        self.processor.display_histogram()
        self.update_window()

    def stretch_histogram(self):
        self.processor.stretch_histogram()
        self.update_window()

    def equalize_histogram(self):
        self.processor.equalize_histogram()
        self.update_window()

    def linear_filters(self):
        self.processor.linear_filters()
        self.update_window()

    def median_filter(self):
        self.processor.median_filter()
        self.update_window()

    def run(self):
        self.master.mainloop()
