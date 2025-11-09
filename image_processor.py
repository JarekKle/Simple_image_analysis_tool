from tkinter import messagebox

from coordinates import Coordinates
from image_manager import ImageManager
import tkinter as tk


class ImageProcessor:
    def __init__(self, manager: ImageManager):
        self.manager = manager

    def change_pixel_color(self, coords: Coordinates):
        root = tk.Toplevel()
        root.title("Wprowadź nowy kolor")
        if self.manager.grayscale:
            tk.Label(root, text="Gray:").grid(row=0, column=0)
            r_var = tk.StringVar(value="0")
            tk.Entry(root, textvariable=r_var).grid(row=0, column=1)

        else:
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
                    if self.manager.grayscale:
                        self.manager.img_modified.putpixel((coords.x, coords.y), r)
                    else:
                        self.manager.img_modified.putpixel((coords.x, coords.y), (r, g, b))
                    self.manager.img_display = self.manager.img_modified.copy()
                    root.destroy()
                else:
                    messagebox.showerror("Błąd", "Wartości muszą być 0–255")
            except ValueError:
                messagebox.showerror("Błąd", "Wprowadź liczby całkowite")

        tk.Button(root, text="OK", command=apply_color).grid(row=3, column=0, columnspan=2)
        root.grab_set()
        root.wait_window()

    def restore_image(self):
        self.manager.img_modified = self.manager.img_original.copy()
        self.manager.img_display = self.manager.img_modified.copy()

    def adjust_brightness(self):
        return

    def display_histogram(self):
        pass

    def stretch_histogram(self):
        return

    def equalize_histogram(self):
        return

    def linear_filters(self):
        pass

    def median_filter(self):
        pass
