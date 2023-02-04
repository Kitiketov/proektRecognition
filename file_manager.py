from PIL import Image,ImageGrab
import os

class File():
    def __init__(self):
        self.path_to_image = 'temp.png'
        self.result_text_path = 'result.txt'

    def grab_from_clipboard(self):
        image = ImageGrab.grabclipboard()
        if image != None:
            image.save(self.path_to_image)
            return self.path_to_image
    
    def grab_from_file(self,_path):
        if os.path.isfile(_path):
            image = Image.open(_path)
            image.save(self.path_to_image)
            return self.path_to_image

    def save_text_to_txt(self,_path,_text):
        if _path:
            with open(_path, "w", encoding = 'UTF-8') as file:
                file.write(_text)
            return self.result_text_path
        

    def delete_temp_image(self):
        os.remove(self.path_to_image)
        pass
if __name__ == '__main__':
    f=File()
    f.delete_temp_image()