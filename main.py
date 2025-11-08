import io
import tkinter as tk
from tkinter import filedialog, Tk

import cairosvg
import numpy as np
from PIL import Image, ImageTk


class ImageManager:
    def __init__(self):
        self.img_original = None
        self.img_modified = None

    def load_image(self, img_name=None):
        if img_name is None:
            img_name = filedialog.askopenfilename(
                title="Wybierz plik obrazu",
                filetypes=[("Image files", ".jpg .jpeg .png .tiff .bmp .svg")]
            )
        if not img_name:
            raise FileNotFoundError("Nie wybrano żadnego pliku.")
        if img_name.lower().endswith('.svg'):
            try:
                png_bytes = cairosvg.svg2png(url=img_name)
                self.img_original = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
                self.img_modified = self.img_original
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć pliku SVG: {e}")
        else:
            try:
                self.img_original = Image.open(img_name)
                self.img_modified = self.img_original
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć obrazu: {e}")

        return self.img_original

    def save_image(self, img_name=None):
        return


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class ImageDisplay:
    def __init__(self, manager: ImageManager):
        self.manager = manager
        self.zoom_factor = 1.0
        self.zoom_step = 1.2
        self.max_zoom = 10.0
        self.pan_step = 20
        self.border_left = Coordinates(0, 0)
        self.wid_display, self.hei_display = self.manager.img_modified.size
        self.border_right = Coordinates(self.wid_display, self.hei_display)
        self.center = Coordinates(self.wid_display // 2, self.hei_display // 2)

    def is_image_grayscale(self):
        img = self.manager.img_original
        if not img:
            return None
        mode = img.mode
        if mode in ("L", "LA"):
            return True
        if mode in ("RGB", "RGBA"):
            arr = np.array(img)
            if arr.ndim == 3 and arr.shape[2] >= 3:
                r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
                return np.array_equal(r, g) and np.array_equal(g, b)

    def calculate_image_bounds(self):
        img = self.manager.img_modified
        width, height = img.size

        self.wid_display = int(width / self.zoom_factor)
        self.hei_display = int(height / self.zoom_factor)

        self.center.x = np.clip(self.center.x, self.wid_display // 2, width - self.wid_display // 2)
        self.center.y = np.clip(self.center.y, self.hei_display // 2, height - self.hei_display // 2)

        self.border_left.x = int(self.center.x - self.wid_display // 2)
        self.border_left.y = int(self.center.y - self.hei_display // 2)
        self.border_right.x = int(self.center.x + self.wid_display // 2)
        self.border_right.y = int(self.center.y + self.hei_display // 2)

        cropped = img.crop((self.border_left.x, self.border_left.y, self.border_right.x, self.border_right.y))

        display_img = cropped.resize((width, height), Image.LANCZOS)
        return display_img

    def get_pixel_coordinates(self):
        pass

    def update_image(self):
        return self.calculate_image_bounds()

    def move(self, dir_x: int, dir_y: int):
        self.center.x = max(0, self.center.x + self.pan_step * dir_x)
        self.center.y = max(0, self.center.y - self.pan_step * dir_y)

    def zoom(self, dir_zoom: int):
        self.zoom_factor = min(max(self.zoom_factor * pow(self.zoom_step, dir_zoom), 1.0), 10.0)


class ImageProcessor:
    def __init__(self, manager: ImageManager):
        self.manager = manager

    def change_pixel_color(self):
        return

    def adjust_brightness(self):
        return

    def stretch_histogram(self):
        return

    def equalize_histogram(self):
        return

    def equalize_channel(self):
        return

    def apply_filter(self):
        return

    def transform_median(self):
        return


class AppWindow:
    def __init__(self, manager: ImageManager, processor: ImageProcessor, display: ImageDisplay):
        self.manager = manager
        self.processor = processor
        self.display = display
        self.master = Tk()
        self.photo = None
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)
        self._setup_window()

    def display_rgb_value(self):
        return

    def display_histogram(self):
        return

    def zoom(self, direction):
        self.display.zoom(direction)
        self.update_image()

    def move(self, dx, dy):
        self.display.move(dx, dy)
        self.update_image()

    def update_image(self):
        img = self.display.update_image()
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)

    def _setup_window(self):
        self.master.title("Image_viewer")
        self._setup_canvas()
        self._setup_status_bar()
        self._setup_controls()
        self._setup_events()

    def _setup_canvas(self):
        self.photo = ImageTk.PhotoImage(self.manager.img_original)
        self.image_label = tk.Label(self.master, image=self.photo)
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _setup_controls(self):
        controls = tk.Frame(self.master)
        controls.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        tk.Button(controls, text="↑", command=lambda: self.move(0, 1), width=8).grid(row=0, column=1)
        tk.Button(controls, text="←", command=lambda: self.move(-1, 0), width=8, height=2).grid(row=1, column=0,
                                                                                                rowspan=2)
        tk.Button(controls, text="+ Zoom in", command=lambda: self.zoom(1), width=12).grid(row=1, column=1)
        tk.Button(controls, text="- Zoom out", command=lambda: self.zoom(-1), width=12).grid(row=2, column=1)
        tk.Button(controls, text="→", command=lambda: self.move(1, 0), width=8, height=2).grid(row=1, column=2,
                                                                                               rowspan=2)
        tk.Button(controls, text="↓", command=lambda: self.move(0, -1), width=8).grid(row=3, column=1)

    def _setup_events(self):
        pass

    def _setup_status_bar(self):
        self.status_bar = tk.Label(self.master, text="Info will be displayed here", anchor="w", relief="sunken")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    test = ImageManager()
    test.load_image("Lena.png")
    test2 = ImageProcessor(test)
    test4 = ImageDisplay(test)
    test3 = AppWindow(test, test2, test4)
    test3.run()
