# pip install easyocr or pip install -r requirements.txt
import easyocr
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageGrab,ImageDraw

from recognition import text_recognition
import tab_detection

import os

class ImgHandler():
    def __init__(self,ui,MyWindow) -> None:
        #self.path = path_to_file
        self.ui = ui
        self.path_to_image = 'temp.png'
        self.result_text_path = 'result.txt'
        self.MyWindow = MyWindow
        self.result_text_path = 'result.txt'
        self.result_draw_path = 'draw.png'
        self.recog = text_recognition.Recognition(image_name =  self.path_to_image)
        self.tab = tab_detection.TabDetector()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.timer = QtCore.QTimer()

    def resize_image(self, img):
        w = 371
        h = 491 
        scale = min(w/img.width, h/img.height)
        new_image = img.resize((int(img.width*scale), int(img.height*scale)))
        return new_image


    def set_plain_text(self,text):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(text)
        pixmap = QPixmap( self.path_to_image)
        self.ui.imageWidget.setPixmap(pixmap)
        os.remove(self.path_to_image)
    

    def show_message(self, widget): 
        widget.setEnabled(True)
        self.timer.timeout.connect(lambda: widget.setEnabled(False))
        self.timer.start(2000)

    def get_path_to_file(self):
        return QtWidgets.QFileDialog.getOpenFileName(self.MyWindow, 'выбрать путь к файлу', '', 'Изображение (*.png *.jpg)')[0]
    
    def get_path_to_save(self):
        return QtWidgets.QFileDialog.getSaveFileName(self.MyWindow, 'выбрать папку для сохранения', 'результат.txt', 'Текстовый документ (*.txt)')[0]
    
    def copy_text(self):
        self.clipboard.setText(self.ui.plainTextEdit.toPlainText())
        self.show_message(self.ui.copyMessage)
    
    def save_text(self):
        path=self.get_path_to_save()
        if path:
            with open(path, "w", encoding = 'UTF-8') as file:
                file.write(self.ui.plainTextEdit.toPlainText())
            self.show_message(self.ui.saveMessage)
            return self.result_text_path

    def text_recognition(self,readFrom ='file'):

        if readFrom =='clipboard':
            image = ImageGrab.grabclipboard()
            if  image is None:
                self.show_message(self.ui.errorMessage)
                return 'Wrong date'
        elif readFrom =='file':
            _path = self.get_path_to_file()
            if os.path.isfile(_path):
                image = Image.open(_path)
            else:
                return 'Error'
        image.save(self.path_to_image)
         
        text,cords = self.recog.start()
        res_img = self.resize_image(Image.open( self.path_to_image))
        res_img.save( self.path_to_image)
        if self.tab.mode:
            tab_count = self.tab.tab_definition(cords)
            tab_text = self.tab.add_tab(text, tab_count)
            self.set_plain_text(tab_text)
        else:
            self.set_plain_text(text)

    def switch_code_mode(self):
        mode = self.recog.switch_mode()
        if mode == 'text':
            self.show_message(self.ui.textModeMessage)
        elif mode == 'code':
            self.show_message(self.ui.codeModeMessage)
    
    def switch_tab_mode(self):
        mode = self.tab.switch_mode()
        # if mode == 'text':
        #     self.show_message(self.ui.textModeMessage)
        # elif mode == 'code':
        #     self.show_message(self.ui.codeModeMessage)


if __name__ == '__main__':
    file_path = 'image/test.png'
    h = ImgHandler(file_path)
    h.text_recognition()
