from PIL import Image
import easyocr

from . import image_preprocessing


class Recognition:
    def __init__(self, image_name) -> None:
        self.mode = 'text'
        self.image_name = image_name

    def start(self):
        # self.image =  Image.open(self.image_name)
        # im_pre = image_preprocessing.ImagePreprocessor(self.image)
        # bin_image = im_pre.convert_color()
        # bin_image.save(self.image_name)
        
        cords = []
        text = ''

        if self.mode == 'text':
            reader = easyocr.Reader(['ru', 'en'])
            result = reader.readtext(self.image_name, detail=1, paragraph=True)
        else:
            reader = easyocr.Reader(['en'],
                        model_storage_directory='custom_EasyOCR/model',
                        user_network_directory='custom_EasyOCR/user_network',
                        recog_network='custom_example',gpu=True) 
            result = reader.readtext(self.image_name, detail=1, paragraph=False, height_ths=1, width_ths=5, x_ths=2 )
        for line in result:
            text += f'{line[1]}\n'
            cords.append(line[0])

        return text, cords
    
    def switch_mode(self):
        if self.mode == 'text':
            self.mode = 'code'
        else:
            self.mode = 'text'
        return self.mode
