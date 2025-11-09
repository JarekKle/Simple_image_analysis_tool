from tkinter import messagebox

import numpy as np

from base_image_handler import BaseImageHandler
from coordinates import Coordinates
import tkinter as tk
from PIL import Image


class GrayscaleImageHandler(BaseImageHandler):

    def convert_to_grayscale(self):
        return self

    def change_pixel_color(self, coords: Coordinates):
        root = tk.Toplevel()
        root.title("Wprowadź nowy kolor")

        tk.Label(root, text="Gray:").grid(row=0, column=0)
        gray_var = tk.StringVar(value="0")
        tk.Entry(root, textvariable=gray_var).grid(row=0, column=1)

        def apply_color():
            try:
                gray = int(gray_var.get())
                if 0 <= gray <= 255:
                    self.img_modified.putpixel((coords.x, coords.y), gray)
                    self.img_display = self.img_modified.copy()
                    root.destroy()
                else:
                    messagebox.showerror("Błąd", "Wartość musi być 0–255")
            except ValueError:
                messagebox.showerror("Błąd", "Wprowadź liczbę całkowitą")

        tk.Button(root, text="OK", command=apply_color).grid(row=3, column=0, columnspan=2)
        root.grab_set()
        root.wait_window()

    def stretch_histogram(self):
        arr = np.array(self.img_modified).astype(np.float32)
        ch_min, ch_max = np.min(arr), np.max(arr)
        if ch_max > ch_min:
            stretched = ((arr - ch_min) / (ch_max - ch_min) * 255).astype(np.uint8)
        else:
            stretched = arr.astype(np.uint8)

        self.img_modified = Image.fromarray(stretched)
        self.img_display = self.img_modified.copy()
