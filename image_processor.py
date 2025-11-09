from image_manager import ImageManager


class ImageProcessor:
    def __init__(self, manager: ImageManager):
        self.manager = manager

    def change_pixel_color(self, coords):
        self.manager.handler.change_pixel_color(coords)

    def convert_to_grayscale(self):
        self.manager.handler = self.manager.handler.convert_to_grayscale()

    def restore_original(self):
        self.manager.restore_original()

    def adjust_brightness(self):
        self.manager.handler.adjust_brightness()

    def stretch_histogram(self):
        self.manager.handler.stretch_histogram()
