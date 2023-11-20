# pip install easyocr or pip install -r requirements.txt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread
from PIL import Image,ImageGrab

from recognition import text_recognition
import tab_detection

import os

class TextRecognitionWorker(QThread):
    recognition_done = QtCore.pyqtSignal(str)

    def __init__(self,ui,path_to_image,tab,recog):
        super().__init__()

        self.ui = ui
        self.path_to_image = path_to_image
        self.tab = tab
        self.recog = recog

    def resize_image(self, img):
        w = self.ui.imageWidget.width()
        h = self.ui.imageWidget.height()
        scale = min(w / img.width, h / img.height)
        new_image = img.resize((int(img.width * scale), int(img.height * scale)))
        return new_image
    
    def run(self):
        text, cords = self.recog.start()
        res_img = self.resize_image(Image.open(self.path_to_image))
        res_img.save(self.path_to_image)

        if self.tab.mode:
            tab_count = self.tab.tab_definition(cords)
            tab_text = self.tab.add_tab(text, tab_count)
            result = tab_text
        else:
            result = text

        self.recognition_done.emit(result)


class ImgHandler():
    def __init__(self, ui, MyWindow) -> None:
        self.ui = ui
        self.MyWindow = MyWindow

        self.path_to_image = 'temp.png'
        self.result_text_path = 'result.txt'

        self.recog = text_recognition.Recognition(self.path_to_image)
        self.tab = tab_detection.TabDetector()
        self.clipboard = QtWidgets.QApplication.clipboard()
        self.timer = QtCore.QTimer()

    def set_plain_text(self, text):
        self.ui.plainTextEdit.setPlainText(text)
        pixmap = QPixmap( self.path_to_image)
        self.ui.imageWidget.setPixmap(pixmap)
        os.remove(self.path_to_image)
    
    def show_message(self, widget, message=''):
        if message:
            widget.setText(message)
        widget.setEnabled(True)
        self.timer.timeout.connect(lambda: widget.setEnabled(False))
        self.timer.start(2000)

    def get_path_to_file(self):
        return QtWidgets.QFileDialog.getOpenFileName(self.MyWindow, 'выбрать путь к файлу', '', 'Изображение (*.png *.jpg *.jpeg)')[0]
    
    def get_path_to_save(self):
        return QtWidgets.QFileDialog.getSaveFileName(self.MyWindow, 'выбрать папку для сохранения', 'результат.txt', 'Текстовый документ (*.txt)')[0]
    
    def copy_text(self):
        self.clipboard.setText(self.ui.plainTextEdit.toPlainText())
        self.show_message(self.ui.messageLabel, 'Copied')
    
    def save_text(self):
        path = self.get_path_to_save()
        if path:
            with open(path, "w", encoding = 'UTF-8') as file:
                file.write(self.ui.plainTextEdit.toPlainText())
            self.show_message(self.ui.messageLabel, 'Saved')
            return self.result_text_path

    def text_recognition(self,readFrom='file'):
        if readFrom == 'clipboard':
            image = ImageGrab.grabclipboard()
            if  image is None:
                self.show_message(self.ui.errorMessage, 'Is not picture')
                return 'Wrong date'
            
        elif readFrom == 'file':
            _path = self.get_path_to_file()
            if os.path.isfile(_path):
                image = Image.open(_path)
            else:
                self.show_message(self.ui.errorMessage, 'No file selected')
                return 'Error'
        image.save(self.path_to_image)

        self.ui.messageLabel.setText('In progress')
        self.timer.blockSignals(True)
        self.ui.messageLabel.setEnabled(True)
        self.change_button_state(False)

        self.workerThread = TextRecognitionWorker(self.ui, self.path_to_image, self.tab, self.recog)
        self.workerThread.recognition_done.connect(self.recognition_completed)
        self.workerThread.finished.connect(self.workerThread.deleteLater)
        self.workerThread.start()
    
    def change_button_state(self,state):
        self.ui.loadButton.setEnabled(state)
        self.ui.copyButton.setEnabled(state)
        self.ui.pasteButton.setEnabled(state)
        self.ui.saveButton.setEnabled(state)
        self.ui.codeMode.setEnabled(state)
        self.ui.tabMode.setEnabled(state)
        
    def recognition_completed(self, text):
        self.set_plain_text(text)
        self.change_button_state(True)
        self.ui.messageLabel.setEnabled(False)
        self.timer.blockSignals(False)

    def switch_code_mode(self):
        mode = self.recog.switch_mode()
        if mode == 'text':
            message = 'TEXT MODE'
        elif mode == 'code':
            message = 'CODE MODE'
        self.show_message(self.ui.messageLabel, message)
    
    def switch_tab_mode(self):
        mode = self.tab.switch_mode()
        if mode == True:
            message = 'TAB ON'
        else:
            message = 'TAB OFF'
        self.show_message(self.ui.messageLabel, message)
