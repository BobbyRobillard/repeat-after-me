from PyQt5 import QtGui
from PyQt5.QtWidgets import *


def setup_navbar(window):
    # Button widget creation, and methods to link to them
    navbar_buttons_details = [
        [QPushButton("Dashboard", window), window.open_dashboard],
        [QPushButton("Quick Record", window), window.start_quick_recording],
        [QPushButton("Help", window), window.open_help]
    ]

    # Set the location of each button,and bind its on_click event to it.
    i, btn_width = 0, 75
    for item in navbar_buttons_details:
        item[0].setGeometry(10 + (i * btn_width), 10, btn_width, 30)
        item[0].clicked.connect(item[1])
        i += 1
