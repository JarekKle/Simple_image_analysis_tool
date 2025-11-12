from tkinter import messagebox

import numpy as np
from matplotlib import pyplot as plt

from base_image_handler import BaseImageHandler
import tkinter as tk
from PIL import Image

from grayscale_image_handler import GrayscaleImageHandler


class ColorImageHandler(BaseImageHandler):

    def convert_to_grayscale(self):
        arr = np.array(self.img_modified, dtype=np.float32)
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        gray = np.clip(gray, 0, 255).astype(np.uint8)
        new_img = Image.fromarray(gray, mode="L")
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

    def display_histogram(self):
        arr = np.array(self.img_modified).astype(np.uint8)
        grayscale_handler = self.convert_to_grayscale()
        grayscale_img = np.array(grayscale_handler.img_modified).astype(np.uint8)

        colors = ('r', 'g', 'b')
        channel_names = ('Red', 'Green', 'Blue')

        fig, axs = plt.subplots(4, 1, figsize=(8, 10))
        fig.suptitle("Histogram kanałów obrazu", fontsize=14)

        for i, (color, name) in enumerate(zip(colors, channel_names)):
            hist, bins = np.histogram(arr[..., i], bins=256, range=(0, 256))
            axs[i].plot(bins[:-1], hist, color=color)
            axs[i].set_title(f"Kanał {name}")
            axs[i].set_xlim(0, 255)

        hist_gray, bins_gray = np.histogram(grayscale_img, bins=256, range=(0, 256))
        axs[3].plot(bins_gray[:-1], hist_gray, color='black')
        axs[3].set_title("Kanał grayscale")
        axs[3].set_xlim(0, 255)

        plt.tight_layout()
        plt.show()

    def equalize_histogram(self):
        arr = np.array(self.img_modified).astype(np.uint8)
        equalized_channels = []
        for i in range(3):
            equalized_channels.append(self.equalize_channel(arr[..., i]))
        equalized = np.stack(equalized_channels, axis=-1).astype(np.uint8)
        self.img_modified = Image.fromarray(equalized)
        self.img_display = self.img_modified.copy()

    def linear_filter(self, kernel):
        arr = np.array(self.img_modified).astype(np.uint8)
        filtered_channels = []
        for i in range(3):
            filtered_channels.append(self.linear_filter_channel(arr[..., i], kernel))
        filtered = np.stack(filtered_channels, axis=-1)
        self.img_modified = Image.fromarray(filtered)
        self.img_display = self.img_modified.copy()

    def median_filter(self, size):
        arr = np.array(self.img_modified).astype(np.uint8)
        filtered_channels = []
        for i in range(3):
            filtered_channels.append(self.median_channel(arr[..., i], size))
        filtered = np.stack(filtered_channels, axis=-1)
        self.img_modified = Image.fromarray(filtered)
        self.img_display = self.img_modified.copy()
