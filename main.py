from app_window import AppWindow
from image_display import ImageDisplay
from image_manager import ImageManager
from image_processor import ImageProcessor

if __name__ == "__main__":
    image_manager = ImageManager()
    image_manager.load_image("Lena.png")
    # image_manager.load_image("Einstein.jpg")
    image_display = ImageDisplay(image_manager)
    image_processor = ImageProcessor(image_manager)
    app_window = AppWindow(image_manager, image_processor, image_display)
    app_window.run()
