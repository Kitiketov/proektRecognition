from PIL import Image
import easyocr

from . import image_preprocessing
from . import postprocessing


class Recognition:
    def __init__(self, image_name) -> None:
        self.mode = 'text'
        self.image_name = image_name
        self.pp = postprocessing.Postprocessing()

    def start(self):
        # self.image =  Image.open(self.image_name)
        # im_pre = image_preprocessing.ImagePreprocessor(self.image)
        # bin_image = im_pre.convert_color()
        # bin_image.save(self.image_name)
        
        cords = []
        raw_text = ''

        if self.mode == 'text':
            reader = easyocr.Reader(['ru', 'en'])
            result = reader.readtext(self.image_name, detail=1, paragraph=False, height_ths=1, width_ths=5, x_ths=2 )
        else:
            reader = easyocr.Reader(['en'],
                        model_storage_directory='custom_EasyOCR/model',
                        user_network_directory='custom_EasyOCR/user_network',
                        recog_network='custom_example',gpu=True) 
            result = reader.readtext(self.image_name, detail=1, paragraph=False, height_ths=1, width_ths=5, x_ths=2 )
        for line in result:
            new_line = ""
            new_line = new_line[:-1]
            raw_text += f'{line[1]}\n'
            cords.append(line[0])
        if self.mode=='code':
            text = self.pp.fuzzy_comparison(raw_text)
        else:
            text = raw_text
        return text, cords
    
    def switch_mode(self):
        mods = {'text':'code','code':'text'}
        self.mode = mods[self.mode]
        return self.mode
