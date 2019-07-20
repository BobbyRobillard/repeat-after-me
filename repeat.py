from pynput.mouse import Button, Controller
from pynput import mouse, keyboard

import time
import tkinter as tk

controller = Controller()

recordings = []

is_recording = False
setting_recording_key = False
recording_key = None

top = tk.Tk()


def handle_keyboard_event(key):
    global is_recording
    global recordings

    global setting_recording_key
    global recording_key

    if setting_recording_key:
        recording_key = key.char
        setting_recording_key = False
        print("Recording key set to: {0}".format(recording_key))

    elif key.char == recording_key:
        handle_recording()

    else:
        play_recording_from_keybind(key.char)


def handle_mouse_event(x, y, button, pressed):
    global recordings
    global is_recording

    if is_recording:
        if pressed:
            recordings[len(recordings) - 1].add_action()


class Recording:
    def __init__(self):
        self.actions = []
        self.key_bind_code = -1

    def add_action(self):
        global controller
        self.actions.append(controller.position)

    def play(self):
        for action in self.actions:
            do_action(action)
            time.sleep(.5)


def do_action(action):
    global controller
    controller.position = (action[0], action[1])
    controller.click(Button.left, 1)


def handle_recording():
    global is_recording

    if not is_recording:
        recordings.append(Recording())
        print("Recording Started")
    else:
        print("Recording Stopped")

    is_recording = not is_recording


def play_recording_from_keybind(char):
    try:
        recordings[int(char) - 1].play()
    except Exception as e:
        print("No recording set to key {0}".format(char))


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
