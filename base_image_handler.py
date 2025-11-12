import tkinter as tk
from enum import Enum

import numpy as np
from PIL import Image


class AdjustmentMethods(Enum):
    ADDITION = 0
    MULTIPLICATION = 1
    POWER = 2


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

    def ask_adjust_brightness_option(self):
        root = tk.Toplevel()
        root.title("Select brightening option")

        option_var = tk.StringVar(value="0")
        values = {"Addition": "0", "Multiplication": "1", "Power": "2"}
        tk.Label(root, text="Select brightening option:").grid(row=0, column=0, columnspan=2, pady=(10, 5))
        i = 1
        for (text, value) in values.items():
            tk.Radiobutton(root, text=text, variable=option_var, value=value).grid(row=i, column=0,
                                                                                   columnspan=2, sticky="w",
                                                                                   padx=20)
            i += 1

        def confirm():
            root.destroy()

        tk.Button(root, text="OK", command=confirm, width=18).grid(row=len(values) + 1, column=0, columnspan=2, pady=10)

        root.grab_set()
        root.wait_window()

        option_value = int(option_var.get())
        option = AdjustmentMethods(option_value)
        return option

    def adjust_brightness(self, option):
        match option:
            case AdjustmentMethods.ADDITION:
                self.additive_adjustment()
            case AdjustmentMethods.MULTIPLICATION:
                self.multiplicative_adjustment()
            case AdjustmentMethods.POWER:
                self.power_adjustment()

    def additive_adjustment(self):
        root = tk.Toplevel()
        root.title("Enter the parameter")
        c_var = tk.StringVar(value="50")
        tk.Label(root, text="L(m,n) + ").grid(row=0, column=0)
        tk.Entry(root, textvariable=c_var).grid(row=0, column=1)

        def brighten():
            c = float(c_var.get())
            arr = np.array(self.img_modified, dtype=np.float32)
            arr = arr + c
            arr = np.clip(arr, 0, 255).astype(np.uint8)
            self.img_modified = Image.fromarray(arr)
            self.img_display = self.img_modified.copy()
            root.destroy()

        tk.Button(root, text="OK", command=brighten, width=18).grid(row=1, column=0, columnspan=3)
        root.grab_set()
        root.wait_window()

    def multiplicative_adjustment(self):
        root = tk.Toplevel()
        root.title("Enter the parameter")
        n_var = tk.StringVar(value="0.5")
        tk.Label(root, text="L(m,n)∙").grid(row=0, column=0)
        tk.Entry(root, textvariable=n_var).grid(row=0, column=1)

        def brighten():
            n = float(n_var.get())
            arr = np.array(self.img_modified)
            arr = arr * n
            arr = np.clip(arr, 0, 255).astype(np.uint8)
            self.img_modified = Image.fromarray(arr)
            self.img_display = self.img_modified.copy()
            root.destroy()

        tk.Button(root, text="OK", command=brighten, width=18).grid(row=1, column=0, columnspan=3)
        root.grab_set()
        root.wait_window()

    def power_adjustment(self):
        root = tk.Toplevel()
        root.title("Enter the parameters")
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

    def create_kernel(self, size):
        root = tk.Toplevel()
        root.title("Input your kernel")
        tk.Label(root, text="Input your kernel").grid(row=0, column=0, columnspan=3)

        kernel_vars = [[tk.StringVar(value="1") for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                tk.Entry(root, textvariable=kernel_vars[i][j], width=5).grid(row=i+1, column=j, padx=2, pady=2)
        def confirm():
            kernel = np.zeros((size, size), dtype=np.float32)
            for i in range(size):
                for j in range(size):
                    try:
                        kernel[i, j] = float(kernel_vars[i][j].get())
                    except ValueError:
                        kernel[i, j] = 0.0
            root.destroy()
            return kernel

        tk.Button(root, text="OK", command=confirm, width=12).grid(row=size+1, column=0, columnspan=size, pady=8)

        root.grab_set()
        root.wait_window()
        kernel = confirm()
        return kernel
    @staticmethod
    def is_kernel_symmetrical(kernel):
        return np.array_equal(kernel, np.rot90(kernel, kernel.shape[0]))

    def ask_linear_filter_parameters(self):
        root = tk.Toplevel()
        root.title("Select linear filter")

        option_var = tk.StringVar(value="0")
        convert_var = tk.BooleanVar(value=False)

        values = {"Low pass": "0", "Prewitt": "1", "Sobel": "2",
                  "Laplace": "3", "Edge detection": "4", "Custom": "x"}

        kernels = {
            "0": {"kernel": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
                  "convert_to_grayscale": False},
            "1": {"kernel": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
                  "convert_to_grayscale": True},
            "2": {"kernel": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
                  "convert_to_grayscale": True},
            "3": {"kernel": np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
                  "convert_to_grayscale": True},
            "4": {"kernel": np.array([[1, 1, 1], [1, -2, -1], [1, -1, -1]]),
                  "convert_to_grayscale": True},
            "x": {"kernel": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
                  "convert_to_grayscale": False},
        }

        tk.Label(root, text="Select linear filter:").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        def update_checkboxes():
            opt = option_var.get()
            settings = kernels[opt]
            convert_to_grayscale = settings["convert_to_grayscale"]
            convert_var.set(convert_to_grayscale)

            convert_cb.config(state=tk.DISABLED if convert_to_grayscale else tk.NORMAL)

        for i, (text, value) in enumerate(values.items(), start=1):
            tk.Radiobutton(root, text=text, variable=option_var, value=value, command=update_checkboxes) \
                .grid(row=i, column=0, columnspan=2, sticky="w", padx=20)

        convert_cb = tk.Checkbutton(root, text="Convert to grayscale", variable=convert_var)
        convert_cb.grid(row=len(values) + 1, column=0)

        def confirm():
            root.destroy()

        tk.Button(root, text="OK", command=confirm, width=18).grid(
            row=len(values) + 2, column=0, columnspan=2, pady=10
        )

        update_checkboxes()

        root.grab_set()
        root.wait_window()
        option_value = option_var.get()
        if option_value == "x":
            kernel = self.create_kernel(3)
        else:
            kernel = kernels[option_value]["kernel"]
        return kernel, convert_var.get()

    def linear_filter_channel(self, channel, kernel):
        kernel_flip = not self.is_kernel_symmetrical(kernel)
        w, h = self.img_modified.size
        kh, kw = kernel.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(channel, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
        g = np.zeros((h, w), dtype=np.float32)
        if kernel_flip:
            gx = np.zeros((h, w), dtype=np.float32)
            gy = np.zeros((h, w), dtype=np.float32)
            kernel_y = np.rot90(kernel, 3)
            for i in range(h):
                for j in range(w):
                    region = padded[i:i+kh, j:j+kw]
                    gx[i, j] = np.sum(region * kernel)
                    gy[i, j] = np.sum(region * kernel_y)
            g = np.sqrt(gx**2 + gy**2)
        else:
            for i in range(h):
                for j in range(w):
                    region = padded[i:i+kh, j:j+kw]
                    g[i, j] = np.sum(region * kernel)
        g[g < 0] = 0
        g -= np.min(g)
        max_val = np.max(g)
        if max_val > 0:
            g = (g / max_val) * 255
        output_matrix = np.clip(g, 0, 255).astype(np.uint8)
        return output_matrix

    def linear_filter(self, kernel):
        ...

    def ask_median_mask_size(self):
        root = tk.Toplevel()
        root.title("Select the size of the median mask")

        size_var = tk.StringVar(value="3")
        sizes = ["3", "5", "7", "9"]

        tk.Label(root, text="Select the size of the median mask:").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        for i, size in enumerate(sizes, start=1):
            tk.Radiobutton(root, text=f"{size}x{size}", variable=size_var, value=size).grid(row=i, column=0,
                                                                                            columnspan=2, sticky="w",
                                                                                            padx=20)

        def confirm():
            root.destroy()

        tk.Button(root, text="OK", command=confirm, width=18).grid(row=len(sizes) + 1, column=0, columnspan=2, pady=10)

        root.grab_set()
        root.wait_window()
        size = int(size_var.get())
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
