from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPoint

import handler
from design import Ui_Form

import sys


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.h = handler.ImgHandler(self.ui, self)

        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle('Black')

        self.ui.loadButton.clicked.connect(lambda: self.h.text_recognition(readFrom = 'file'))
        self.ui.exitButton.clicked.connect(lambda: exit(0))
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.ui.copyButton.clicked.connect(lambda: self.h.copy_text())
        self.ui.pasteButton.clicked.connect(lambda: self.h.text_recognition(readFrom = 'clipboard'))
        self.ui.saveButton.clicked.connect(lambda: self.h.save_text())
        self.ui.codeMode.clicked.connect(lambda: self.h.switch_code_mode())
        self.ui.tabMode.clicked.connect(lambda: self.h.switch_tab_mode())
        

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())