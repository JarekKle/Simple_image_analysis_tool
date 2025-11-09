import numpy as np
from PIL import Image

from coordinates import Coordinates
from image_manager import ImageManager


class ImageDisplay:
    def __init__(self, manager: ImageManager):
        self.manager = manager
        self.zoom_factor = 1.0
        self.zoom_step = 1.2
        self.max_zoom = 10.0
        self.pan_step = 20
        self.border_left = Coordinates(0, 0)
        self.wid_display, self.hei_display = self.manager.handler.img_display.size
        self.border_right = Coordinates(self.wid_display, self.hei_display)
        self.center = Coordinates(self.wid_display // 2, self.hei_display // 2)

    def calculate_image_bounds(self):
        img = self.manager.handler.img_modified
        img_w, img_h = img.size

        wid_display = int(img_w / self.zoom_factor)
        hei_display = int(img_h / self.zoom_factor)

        self.center.x = np.clip(self.center.x, wid_display // 2, img_w - wid_display // 2)
        self.center.y = np.clip(self.center.y, hei_display // 2, img_h - hei_display // 2)

        left = int(self.center.x - wid_display // 2)
        top = int(self.center.y - hei_display // 2)
        right = left + wid_display
        bottom = top + hei_display

        self.border_left.x, self.border_left.y = left, top
        self.border_right.x, self.border_right.y = right, bottom

        cropped = img.crop((left, top, right, bottom))

        display_img = cropped.resize(
            (int(wid_display * self.zoom_factor), int(hei_display * self.zoom_factor)),
            resample=Image.NEAREST
        )

        return display_img

    def get_pixel_value(self, coords: Coordinates):
        img = self.manager.handler.img_modified
        if not img:
            return None

        pixel = img.getpixel(coords)
        if self.manager.is_image_grayscale(img):
            pixel = (pixel, pixel, pixel)
        return pixel

    def update_image(self):
        return self.calculate_image_bounds()

    def move(self, dir_x: int, dir_y: int):
        self.center.x = max(0, self.center.x + self.pan_step * dir_x)
        self.center.y = max(0, self.center.y - self.pan_step * dir_y)

    def zoom(self, dir_zoom: int):
        self.zoom_factor = round(min(max(self.zoom_factor * pow(self.zoom_step, dir_zoom), 1.0), 10.0), 2)
