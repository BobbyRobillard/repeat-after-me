from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from utils import get_current_profile

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        labelA = QLabel(self)

        current_profile_name = get_current_profile("test")[2]
        print(str(current_profile_name))
        labelA.setText(current_profile_name)
        self.setGeometry(100, 100, 300, 200)
        self.show()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
