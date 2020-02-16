from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from utils import get_current_profile, add_profile, get_profiles, get_recordings

from graphics import setup_navbar

from HelpScreen import HelpWindow

from QuickRecordScreen import QuickRecordWindow

import sys


class Window(QMainWindow):
    # ---------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.gui_setup()
        self.show()
    # ---------------------------------------------------------------------
    def gui_setup(self):
        # Top buttons to navigate between windows
        setup_navbar(self)

        self.setup_current_profile()

        # Shows all available profiles a user has
        self.labelB = QLabel(self)
        self.labelB.setGeometry(10, 175, 200, 125)
        profile_names = [profile['name'] for profile in get_profiles()]
        self.labelB.setText("YOUR PROFILES:\n" + ", \n".join(profile_names))

        # Add a new profile
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(10, 120, 240, 30)

        button = QPushButton("Save New Profile", self)
        button.setGeometry(260, 120, 30, 30)
        button.clicked.connect(self.add_profile_btn_click)

        # Set main window size
        self.setGeometry(100, 50, 500, 500)
    # ---------------------------------------------------------------------
    def setup_current_profile(self):
        # Displays current profile to active user
        self.labelA = QLabel(self)
        self.labelA.setGeometry(10, 60, 200, 50)
        current_profile = get_current_profile()

        label_text = (
            "CURRENT PROFILE:\n" +
            current_profile['name'] + "\nRecordings: \n" +
            ", \n".join([recording['name'] for recording in get_recordings(current_profile['profile_id'])])
        )

        self.labelA.setText(label_text)
    # ---------------------------------------------------------------------
    def add_profile_btn_click(self):
        profile_name = self.textbox.text()
        # Replace with actual code to get current user's id
        add_profile(profile_name)
        self.labelA.setText("Added profile: {0}".format(profile_name))

        profile_names = [profile['name'] for profile in get_profiles()]
        self.labelB.setText("YOUR PROFILES:\n" + ", \n".join(profile_names))
    # ---------------------------------------------------------------------
    def open_help(self):
        self.window = HelpWindow()
    # ---------------------------------------------------------------------
    def open_dashboard(self):
        print("Opening Dashboard")
    # ---------------------------------------------------------------------
    def start_quick_recording(self):
        self.window = QuickRecordWindow()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
