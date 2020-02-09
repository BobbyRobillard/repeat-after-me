from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from utils import get_current_profile, add_profile

import sys


class Window(QMainWindow):
    def __init__(self):
        username = "test"

        super().__init__()

        self.labelA = QLabel(self)
        self.labelA.setGeometry(10, 10, 200, 30)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(10, 60, 240, 30)
        button = QPushButton("+", self)
        button.setGeometry(260, 60, 30, 30)
        button.clicked.connect(self.add_profile_btn_click)

        current_profile_name = get_current_profile(username)[2]
        self.labelA.setText("Current Profile: " + current_profile_name)
        self.setGeometry(100, 50, 500, 500)
        self.show()

    def add_profile_btn_click(self, user_id):
        profile_name = self.textbox.text()
        # Replace with actual code to get current user's id
        add_profile(1, profile_name)
        self.labelA.setText("Added profile: {0}".format(profile_name))


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
