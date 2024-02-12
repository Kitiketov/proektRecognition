from PIL import Image, ImageOps


class ImagePreprocessor:
    def __init__(self, image) -> None:
        self.image = image
    
    def _find_average_color(self, image):
        color = 0
        pixels = image.load()
        height, width = image.size

        for i in range(height):
            for j in range(width):
                color += pixels[i, j]
        color /= (height * width)

        return color
    
    def _image_binarization(self, image):
        height, width = image.size
        pixels = image.load()

        img = Image.new('1', (height, width))
        new_pixels = img.load()

        for i in range(height):
            for j in range(width):
                if pixels[i, j] >= 200:
                    new_pixels[i, j] = 255
                else:
                   new_pixels[i, j] = 0

        return img
    
    
    def convert_color(self):
        converted_image = self.image.convert('L')

        color = self._find_average_color(converted_image)
        if color < 200:
            converted_image = ImageOps.invert(converted_image)
        
        bin_image = self._image_binarization(converted_image)

        return bin_image