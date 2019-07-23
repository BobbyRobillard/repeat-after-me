from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput import mouse, keyboard

import time
import tkinter as tk

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

recordings = []

is_recording = False
setting_recording_key = False
recording_key = None

top = tk.Tk()


def handle_keyboard_event(key):
    global is_playing
    global is_recording
    global recordings

    global setting_recording_key
    global recording_key

    try:
        if setting_recording_key:
            recording_key = key.char
            setting_recording_key = False
            print("Recording key set to: {0}".format(recording_key))

        elif key.char == recording_key:
            handle_recording()

        elif is_recording:
            recordings[len(recordings) - 1].actions.append(KeyboardAction(key.char))

        else:
            play_recording_from_keybind(key.char)

    except AttributeError:
        print("Special key: {0} pressed".format(key))


def handle_mouse_event(x, y, button, pressed):
    global recordings
    global is_recording

    if is_recording:
        if pressed:
            recordings[len(recordings) - 1].actions.append(MouseAction(x, y, button))


class MouseAction(object):
    def __init__(self, x, y, button):
        self.x = x
        self.y = y
        self.button = button

    def __str__(self):
        return "Mouse press: ({0}, {1})".format(self.x, self.y)

    def do_action(self):
        global mouse_controller
        mouse_controller.position = (self.x, self.y)
        mouse_controller.click(Button.left, 1)


class KeyboardAction(object):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return "Keypress: {0}".format(self.char)

    def do_action(self):
        global keyboard_controller
        # print("DOING KEYBOARD ACTION")
        keyboard_controller.type(self.char)


class Recording(object):
    def __init__(self):
        self.actions = []
        self.key_bind_code = -1

    def __str__(self):
        return str(self.actions)

    def play(self):
        for action in self.actions:
            action.do_action()
            time.sleep(0.5)


def handle_recording():
    global is_recording

    if not is_recording:
        recordings.append(Recording())
        print("Recording Started")
    else:
        print("Recording Stopped")

    is_recording = not is_recording


def play_recording_from_keybind(char):
    global keyboard_listener
    keyboard_listener.stop()
    try:
        recordings[int(char) - 1].play()
    except Exception as e:
        print("No recording set to key {0}".format(char))
    keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
    keyboard_listener.start()


def set_recording_key():
    global setting_recording_key

    setting_recording_key = True
    print("Please enter the key to start/stop recording...\n")


button = tk.Button(top, text="Set Recording Key", command=set_recording_key)
button.pack()

keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

top.mainloop()
