# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from OtherWindow import Ui_OtherWindow


class Ui_MainWindow(object):

    def setupUI(self, MainWindow):
        MainWindow.resize(300, 300)
        self.button = QtWidgets.QPushButton("+", MainWindow)
        self.button.setGeometry(260, 120, 100, 30)
        self.button.clicked.connect(self.openWindow)

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_OtherWindow()
        self.ui.setupUi(self.window)
        # MainWindow.hide()
        self.window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
