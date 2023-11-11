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
        super().__init__()
        self.ui = Ui_Form()
        self.h = handler.ImgHandler(self.ui,self)
       
        
        self.ui.setupUi(self)
        self.gif = QtGui.QMovie('load.gif') 
        self.gif.setScaledSize( QtCore.QSize(50,50))
        self.gif.setBackgroundColor(QColor(44, 47, 51))
        self.ui.loadgif.setMovie(self.gif)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle('Vce to text')

        self.ui.loadButton.clicked.connect(lambda: self.h.text_recognition(readFrom ='file'))
        self.ui.exitButton.clicked.connect(lambda: exit(0))
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.ui.copyButton.clicked.connect(lambda: self.h.copy_text())
        self.ui.pasteButton.clicked.connect(lambda: self.h.text_recognition(readFrom ='clipboard'))
        self.ui.saveButton.clicked.connect(lambda: self.h.save_text())
        self.ui.codeMode.clicked.connect(lambda: self.h.switch_code_mode())
        self.ui.tabMode.clicked.connect(lambda: self.h.switch_tab_mode())


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




    






            

    
    
    # def save_and_start_recognition(self,readFrom):

    #     if readFrom =='clipboard':
    #         image = ImageGrab.grabclipboard()
    #         if  image is None:
    #             self.show_message(self.ui.errorMessage)
    #             return 'Wrong date'

    #     elif readFrom =='file':
    #         path = self.get_path_to_file()
    #         if path:
    #             if os.path.isfile(path):
    #                 image = Image.open(path)
    #         else:
    #             return 'Error'
    #     image.save(self.path_to_image)
    #     #TODO

    #     #self.ui.loadgif.setEnabled(True)
    #     self.gif.start()

    #     text = self.h.text_recognition()
    #     self.set_plain_text(text)

    #     self.gif.stop()
    #     self.ui.loadgif.setEnabled(False)

        


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())