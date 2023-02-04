from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap,QColor
import sys
import handler
from design import Ui_Form
from PIL import Image,ImageGrab
import os


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.path_to_image = 'temp.png'
        self.result_text_path = 'result.txt'
        super(MyWindow, self).__init__()
        self.ui = Ui_Form()
        self.h = handler.ImgHandler()
        self.clipboard = QtWidgets.QApplication.clipboard()
        
        self.ui.setupUi(self)
        self.gif = QtGui.QMovie('load.gif') 
        self.gif.setScaledSize( QtCore.QSize(50,50))
        self.gif.setBackgroundColor(QColor(44, 47, 51))
        self.ui.loadgif.setMovie(self.gif)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle('Vce to text')

        self.ui.loadButton.clicked.connect(lambda: self.save_and_start_recognition(readFrom ='file'))
        self.ui.exitButton.clicked.connect(lambda: exit(0))
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.ui.copyButton.clicked.connect(lambda: self.copy_text())
        self.ui.pasteButton.clicked.connect(lambda: self.save_and_start_recognition(readFrom ='clipboard'))
        self.ui.saveButton.clicked.connect(lambda: self.save_text())

        self.timer = QtCore.QTimer()
        #self.time = QtCore.QTime(0, 0, 0)

    def mouseMoveEvent(self, event):
        #print(event.pos(),event.globalPos(),self.x(),self.y())
        delta = QPoint ( event.pos())
        mousecord = QPoint (event.globalPos())
        if delta.y() == 30:
            self.tempcord = QPoint(event.pos())
        self.move(mousecord.x() - self.tempcord.x(),mousecord.y() -self.tempcord.y())

    def mousePressEvent(self, event): 
        self.tempcord = QPoint(event.pos())


    def show_message(self, widget): 
        widget.setEnabled(True)
        self.timer.timeout.connect(lambda: widget.setEnabled(False))
        self.timer.start(2000)

    def get_path_to_file(self):
        return QtWidgets.QFileDialog.getOpenFileName(self, 'выбрать путь к файлу', '', 'Изображение (*.png *.jpeg)')[0]

    def get_path_to_save(self):
        return QtWidgets.QFileDialog.getSaveFileName(self, 'выбрать папку для сохранения', 'результат.txt', 'Текстовый документ (*.txt)')[0]

    def set_plain_text(self,text):
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(text)
        pixmap = QPixmap('temp.png')
        self.ui.imageWidget.setPixmap(pixmap)
        os.remove(self.path_to_image)
    
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
            

    
    
    def save_and_start_recognition(self,readFrom):

        if readFrom =='clipboard':
            image = ImageGrab.grabclipboard()
            if  image is None:
                self.show_message(self.ui.errorMessage)
                return 'Wrong date'

        elif readFrom =='file':
            path = self.get_path_to_file()
            if path:
                if os.path.isfile(path):
                    image = Image.open(path)
            else:
                return 'Error'
        image.save(self.path_to_image)
        #TODO

        #self.ui.loadgif.setEnabled(True)
        self.gif.start()

        text = self.h.text_recognition()
        self.set_plain_text(text)

        self.gif.stop()
        self.ui.loadgif.setEnabled(False)

        


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())