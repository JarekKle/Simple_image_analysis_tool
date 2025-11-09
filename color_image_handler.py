from tkinter import messagebox

import numpy as np

from base_image_handler import BaseImageHandler
import tkinter as tk
from PIL import Image
from grayscale_image_handler import GrayscaleImageHandler


class ColorImageHandler(BaseImageHandler):

    def convert_to_grayscale(self):
        new_img = self.img_modified.convert("L")
        return GrayscaleImageHandler(new_img)
    def change_pixel_color(self, coords):
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
                    self.img_modified.putpixel((coords.x, coords.y), (r, g, b))
                    self.img_display = self.img_modified.copy()
                    root.destroy()
                else:
                    messagebox.showerror("Błąd", "Wartości muszą być 0–255")
            except ValueError:
                messagebox.showerror("Błąd", "Wprowadź liczby całkowite")

        tk.Button(root, text="OK", command=apply_color).grid(row=3, column=0, columnspan=2)
        root.grab_set()
        root.wait_window()

    def stretch_histogram(self):
        arr = np.array(self.img_modified).astype(np.float32)
        stretched_channels = []
        for i in range(3):
            ch = arr[..., i]
            ch_min, ch_max = np.min(ch), np.max(ch)
            if ch_max > ch_min:
                ch_stretched = ((ch - ch_min) / (ch_max - ch_min) * 255)
            else:
                ch_stretched = ch.copy()
            stretched_channels.append(ch_stretched)
        stretched = np.stack(stretched_channels, axis=-1).astype(np.uint8)
        self.img_modified = Image.fromarray(stretched)
        self.img_display = self.img_modified.copy()

