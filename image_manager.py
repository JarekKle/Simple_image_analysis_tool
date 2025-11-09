import io
from tkinter import filedialog

import cairosvg
import numpy as np
from PIL import Image

from color_image_handler import ColorImageHandler
from grayscale_image_handler import GrayscaleImageHandler


class ImageManager:
    def __init__(self):
        self.handler = None
        self.original_handler = None

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

        self._assign_handler(img)
        self.original_handler = self.handler
        return self.handler.img_modified

    def replace_image(self, new_img):
        self._assign_handler(new_img)

    def _assign_handler(self, img):
        if self.is_image_grayscale(img):
            self.handler = GrayscaleImageHandler(img)
        else:
            self.handler = ColorImageHandler(img)

    def save_image(self, img_name=None):
        return

    def convert_to_grayscale(self):
        new_handler = self.handler.convert_to_grayscale()
        if new_handler is not self.handler:
            self.handler = new_handler

    def restore_original(self):
        self.handler = self.original_handler
        self.handler.restore_original()
    @staticmethod
    def is_image_grayscale(img):
        if img.mode == "L":
            return True
        if img.mode in ("RGB", "RGBA"):
            arr = np.array(img)
            return np.allclose(arr[..., 0], arr[..., 1]) and np.allclose(arr[..., 1], arr[..., 2])
        return False
