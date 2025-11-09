from tkinter import messagebox

from base_image_handler import BaseImageHandler
from coordinates import Coordinates
import tkinter as tk


class GrayscaleImageHandler(BaseImageHandler):
    def __init__(self, img):
        self.img_original = img.convert("L")
        self.img_modified = self.img_original.copy()
        self.img_display = self.img_original.copy()
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
