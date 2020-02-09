from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from utils import get_current_profile

import sys


def on_click():
    AddProfileWindow()


class AddProfileWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 500, 500)
        self.show()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        labelA = QLabel(self)
        labelA.setGeometry(10, 10, 200, 50)
        button = QPushButton("+", self)
        button.setGeometry(150, 10, 50, 50)
        button.clicked.connect(on_click)

        current_profile_name = get_current_profile("test")[2]
        labelA.setText(current_profile_name)
        self.setGeometry(100, 50, 500, 500)
        self.show()





App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
