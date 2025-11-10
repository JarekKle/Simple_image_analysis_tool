import tkinter as tk

import numpy as np
from PIL import Image


class BaseImageHandler:
    def __init__(self, img):
        self.img_original = img
        self.img_modified = self.img_original.copy()
        self.img_display = self.img_original.copy()

    def change_pixel_color(self, coords):
        ...

    def restore_original(self):
        self.img_modified = self.img_original.copy()
        self.img_display = self.img_modified.copy()

    def convert_to_grayscale(self):
        ...

    def adjust_brightness(self):
        root = tk.Toplevel()
        root.title("Wprowadź parametry")
        c_var = tk.StringVar(value="1")
        n_var = tk.StringVar(value="2")
        tk.Entry(root, textvariable=c_var).grid(row=0, column=0)
        tk.Label(root, text="∙(L(m,n))^").grid(row=0, column=1)
        tk.Entry(root, textvariable=n_var).grid(row=0, column=2)

        def brighten():
            c = float(c_var.get())
            n = float(n_var.get())
            arr = np.array(self.img_modified).astype(np.float32)
            arr = c * np.power(arr / 255.0, n) * 255
            arr = np.clip(arr, 0, 255).astype(np.uint8)
            self.img_modified = Image.fromarray(arr)
            self.img_display = self.img_modified.copy()
            root.destroy()

        tk.Button(root, text="OK", command=brighten, width=18).grid(row=1, column=0, columnspan=3)
        root.grab_set()
        root.wait_window()

    def display_histogram(self):
        ...

    def stretch_histogram(self):
        ...

    @staticmethod
    def equalize_channel(channel):
        m = 256
        n = channel.size

        nk = np.bincount(channel.flatten(), minlength=m)
        pk = nk / n
        sk = np.cumsum(pk)

        s0 = sk[np.nonzero(sk)][0]
        lut = ((sk - s0) / (1 - s0) * (m - 1))
        lut = np.clip(lut, 0, m - 1).astype(np.uint8)
        channel_eq = lut[channel]
        return channel_eq

    def equalize_histogram(self):
        ...

    def linear_filters(self):
        ...

    def ask_median_mask_size(self):
        root = tk.Toplevel()
        root.title("Wybierz rozmiar maski medianowej")

        size_var = tk.StringVar(value="3")
        sizes = ["3", "5", "7", "9"]

        tk.Label(root, text="Wybierz rozmiar maski:").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        for i, size in enumerate(sizes, start=1):
            tk.Radiobutton(root, text=f"{size}x{size}", variable=size_var, value=size).grid(row=i, column=0,
                                                                                            columnspan=2, sticky="w",
                                                                                            padx=20)

        def confirm():
            mask_size = int(size_var.get())
            self.median_filter(mask_size)
            root.destroy()
            return mask_size

        tk.Button(root, text="OK", command=confirm, width=18).grid(row=len(sizes) + 1, column=0, columnspan=2, pady=10)

        root.grab_set()
        root.wait_window()
        size = confirm()
        return size

    def median_filter(self, size):
        ...

    def median_channel(self, channel, size):
        w, h = self.img_modified.size
        pad_h, pad_w = size // 2, size // 2
        padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
        g = np.zeros((h, w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                region = padded[i:i + size, j:j + size]
                g[i, j] = np.mean(region)
        output_matrix = np.clip(g, 0, 255).astype(np.uint8)
        return output_matrix
