import io
import tkinter as tk
from tkinter import filedialog, Tk, simpledialog, messagebox

import cairosvg
import numpy as np
from PIL import Image, ImageTk


class ImageManager:
    def __init__(self):
        self.img_original = None
        self.img_modified = None
        self.img_display = None

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
                self.img_display = self.img_original
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć pliku SVG: {e}")
        else:
            try:
                self.img_original = Image.open(img_name)
                self.img_modified = self.img_original
                self.img_display = self.img_original
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć obrazu: {e}")

        return self.img_modified

    def save_image(self, img_name=None):
        return


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y


class ImageDisplay:
    def __init__(self, manager: ImageManager):
        self.manager = manager
        self.zoom_factor = 1.0
        self.zoom_step = 1.2
        self.max_zoom = 10.0
        self.pan_step = 20
        self.border_left = Coordinates(0, 0)
        self.wid_display, self.hei_display = self.manager.img_display.size
        self.border_right = Coordinates(self.wid_display, self.hei_display)
        self.center = Coordinates(self.wid_display // 2, self.hei_display // 2)

    def is_image_grayscale(self):
        img = self.manager.img_modified
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
        img = self.manager.img_display
        img_w, img_h = img.size

        wid_display = int(img_w / self.zoom_factor)
        hei_display = int(img_h / self.zoom_factor)

        self.center.x = np.clip(self.center.x, wid_display // 2, img_w - wid_display // 2)
        self.center.y = np.clip(self.center.y, hei_display // 2, img_h - hei_display // 2)

        left = int(self.center.x - wid_display // 2)
        top = int(self.center.y - hei_display // 2)
        right = left + wid_display
        bottom = top + hei_display

        self.border_left.x, self.border_left.y = left, top
        self.border_right.x, self.border_right.y = right, bottom

        cropped = img.crop((left, top, right, bottom))

        display_img = cropped.resize(
            (int(wid_display * self.zoom_factor), int(hei_display * self.zoom_factor)),
            resample=Image.NEAREST
        )

        return display_img

    def get_pixel_value(self, coords: Coordinates):
        img = self.manager.img_modified
        if not img:
            return None

        pixel = img.getpixel(coords)
        if isinstance(pixel, int):
            pixel = (pixel, pixel, pixel)
        return pixel

    def update_image(self):
        return self.calculate_image_bounds()

    def move(self, dir_x: int, dir_y: int):
        self.center.x = max(0, self.center.x + self.pan_step * dir_x)
        self.center.y = max(0, self.center.y - self.pan_step * dir_y)

    def zoom(self, dir_zoom: int):
        self.zoom_factor = round(min(max(self.zoom_factor * pow(self.zoom_step, dir_zoom), 1.0), 10.0), 2)


class ImageProcessor:
    def __init__(self, manager: ImageManager):
        self.manager = manager

    def change_pixel_color(self, coords: Coordinates):
        root = tk.Toplevel()
        root.title("Wprowadź nowy kolor")

        tk.Label(root, text="R:").grid(row=0, column=0)
        tk.Label(root, text="G:").grid(row=1, column=0)
        tk.Label(root, text="B:").grid(row=2, column=0)

        r_var = tk.StringVar(value="0")
        g_var = tk.StringVar(value="0")
        b_var = tk.StringVar(value="0")

        tk.Entry(root, textvariable=r_var).grid(row=0, column=1)
        tk.Entry(root, textvariable=g_var).grid(row=1, column=1)
        tk.Entry(root, textvariable=b_var).grid(row=2, column=1)

        def apply_color():
            try:
                r = int(r_var.get())
                g = int(g_var.get())
                b = int(b_var.get())
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    self.manager.img_modified.putpixel((coords.x, coords.y), (r, g, b))
                    root.destroy()
                else:
                    messagebox.showerror("Błąd", "Wartości muszą być 0–255")
            except ValueError:
                messagebox.showerror("Błąd", "Wprowadź liczby całkowite")

        tk.Button(root, text="OK", command=apply_color).grid(row=3, column=0, columnspan=2)
        root.grab_set()
        root.wait_window()
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
        self.current_pixel_rgb = (0, 0, 0)
        self.current_pixel_coords = Coordinates(0, 0)
        self.real_pixel_coords = Coordinates(0, 0)
        self.master.columnconfigure(0, weight=3)
        self.master.columnconfigure(1, weight=1)
        self._setup_window()

    def display_rgb_value(self):
        return

    def display_histogram(self):
        return

    def zoom(self, direction):
        self.display.zoom(direction)
        self.update_window()

    def move(self, dx, dy):
        self.display.move(dx, dy)
        self.update_window()

    def update_image(self):
        img = self.display.update_image()
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)

    def update_status_bar(self):
        r, g, b = self.current_pixel_rgb
        x, y = self.real_pixel_coords
        zoom = self.display.zoom_factor
        self.status_bar.config(
            text=f"Zoom: {zoom}x | Pozycja: ({x}, {y}) | RGB: ({r}, {g}, {b})"
        )

    def update_window(self):
        self.display.calculate_image_bounds()
        self.update_image()
        self.update_status_bar()

    def get_pixel_value(self, event):
        width, height = self.manager.img_display.size
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

    def _setup_window(self):
        self.master.title("Image_viewer")
        self._setup_canvas()
        self._setup_status_bar()
        self._setup_controls()
        self._setup_events()

    def _setup_canvas(self):
        width, height = self.manager.img_modified.size
        self.photo = ImageTk.PhotoImage(self.manager.img_modified)
        self.image_label = tk.Label(self.master, image=self.photo, width=width, height=height)
        self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _setup_controls(self):
        controls = tk.Frame(self.master)
        controls.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.button_up = tk.Button(controls, text="↑", width=8)
        self.button_up.grid(row=0, column=1)

        self.button_left = tk.Button(controls, text="←", width=8, height=2)
        self.button_left.grid(row=1, column=0, rowspan=2)

        self.button_zoom_in = tk.Button(controls, text="+ Zoom in", width=12)
        self.button_zoom_in.grid(row=1, column=1)

        self.button_zoom_out = tk.Button(controls, text="- Zoom out", width=12)
        self.button_zoom_out.grid(row=2, column=1)

        self.button_right = tk.Button(controls, text="→", width=8, height=2)
        self.button_right.grid(row=1, column=2, rowspan=2)

        self.button_down = tk.Button(controls, text="↓", width=8)
        self.button_down.grid(row=3, column=1)

    def change_pixel_color(self, event):
        self.processor.change_pixel_color(self.real_pixel_coords)
        self.update_window()

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

    def _setup_status_bar(self):
        self.status_bar = tk.Label(self.master, text="Info will be displayed here", anchor="w", relief="sunken")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    image_manager = ImageManager()
    image_manager.load_image("Lena.png")
    image_processor = ImageProcessor(image_manager)
    image_display = ImageDisplay(image_manager)
    app_window = AppWindow(image_manager, image_processor, image_display)
    app_window.run()
