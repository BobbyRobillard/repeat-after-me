# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OtherWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *

import webbrowser


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.labelA = QLabel(self)
        self.labelA.setGeometry(10, 10, 200, 30)
        self.labelA.setText("Help Screen")

        documentation_button = QPushButton("Open Documentation", self)
        forum_button = QPushButton("Open Forum", self)

        documentation_button.setGeometry(10, 40, 125, 30)
        forum_button.setGeometry(135, 40, 125, 30)

        documentation_button.clicked.connect(self.open_documentation)
        forum_button.clicked.connect(self.open_forum)

        self.setGeometry(200, 150, 500, 500)
        self.show()

    def open_documentation(self):
        webbrowser.open("https://68.183.125.253", new=2)

    def open_forum(self):
        webbrowser.open("https://68.183.125.253", new=2)
