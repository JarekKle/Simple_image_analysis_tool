import io
from tkinter import filedialog

import cairosvg
import numpy as np
from PIL import Image


class ImageManager:
    def __init__(self):
        self.img_original = None
        self.img_modified = None
        self.img_display = None
        self.grayscale = False

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
                img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć pliku SVG: {e}")
        else:
            try:
                img = Image.open(img_name)
            except Exception as e:
                raise TypeError(f"Nie udało się otworzyć obrazu: {e}")

        self.img_modified = img.copy()

        if self.is_image_grayscale():
            img = img.convert("L")
            self.grayscale = True
        else:
            self.grayscale = False

        self.img_original = img.copy()
        self.img_modified = img.copy()
        self.img_display = img.copy()

        return self.img_modified

    def save_image(self, img_name=None):
        return

    def is_image_grayscale(self):
        img = self.img_modified
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
        return False
