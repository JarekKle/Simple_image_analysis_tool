import numpy as np
from PIL import Image
import tkinter as tk

class BaseImageHandler:
    def __init__(self, img):
        self.img_original = img.convert("RGB")
        self.img_modified = self.img_original.copy()
        self.img_display = self.img_original.copy()
    def change_pixel_color(self, coords): ...

    def restore_original(self):
        self.img_modified = self.img_original.copy()
        self.img_display = self.img_modified.copy()

    def convert_to_grayscale(self): ...
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

    def display_histogram(self): ...
    def stretch_histogram(self): ...
    def equalize_histogram(self): ...
    def linear_filters(self): ...
    def median_filter(self): ...