import cv2
import numpy as np

class ImagePreprocessor:
    def __init__(self) -> None:
        self.image = cv2.imread('temp4.png')


    def _find_average_color(self,image):
        color = 0
        height, width = image.shape[:2]
        for i in range(height):
            for j in range(width):
                color += image[i, j]
        color /= (height * width)
        return color
    
    def _image_binarization(self,image):
        height, width = image.shape[:2]
        img = np.zeros((height,width,3), np.uint8)
        for i in range(height):
            for j in range(width):
                if image[i, j] >= 80:
                    img[i, j] = 255
                else:
                    img[i, j] = 0
        return img
    
    
    def convert_color(self):
        converted_image = cv2.cvtColor(self.image,  cv2.COLOR_BGR2GRAY)

        color = self._find_average_color(converted_image)
        if color > 80:
            converted_image = cv2.bitwise_not(converted_image)
        
        img = self. _image_binarization(converted_image)

        cv2.imshow("color converted image", converted_image)
        k = cv2.waitKey(0)
        cv2.imshow("white and black image", img)
        k = cv2.waitKey(0)