import image_preprocessing
import text_regions_detection


class Recognition:
    def __init__(self) -> None:
        pass

    def start(self):
        im_pre = image_preprocessing.ImagePreprocessor()
        im_pre.convert_color()
        text_regions_detection()

if __name__ == "__main__":
    r = Recognition()
    r.start()