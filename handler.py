# pip install easyocr or pip install -r requirements.txt
import easyocr
from PIL import Image,ImageGrab,ImageDraw




class ImgHandler():
    def __init__(self) -> None:
        #self.path = path_to_file
        self.result_text_path = 'result.txt'
        self.result_draw_path = 'draw.png'

    def resize_image(self, img):
        w = 371
        h = 491 
        scale = min(w/img.width, h/img.height)
        new_image = img.resize((int(img.width*scale), int(img.height*scale)))
        return new_image

    # def save_image(self):
    #     image = Image.open(self.path)
    #     image.save('temp.png')

    # def grab_from_clipboard(self):

    #     image = ImageGrab.grabclipboard()
    #     if image != None:
    #         image.save(self.path)
    #         return True


    def text_recognition(self):
        reader = easyocr.Reader(['ru', 'en'])
        text=''
        result = reader.readtext('temp.png', detail=1, paragraph=True)

        
        for line in result:

            text+=f"{line[1]}\n"
        res_img = self.resize_image(Image.open('temp.png'))
        res_img.save('temp.png')
        return text

    # def draw_polygon(self, draw, cord):
    #     xy = [tuple(i) for i in cord]
    #     draw.polygon(xy, outline='green', width=2)
    #     return draw

    # def create_image(self):
    #     image = Image.open(self.result_draw_path)
    #     draw = ImageDraw.Draw(image)
    #     return image, draw


if __name__ == '__main__':
    file_path = 'image/test.png'
    h = ImgHandler(file_path)
    h.text_recognition()
