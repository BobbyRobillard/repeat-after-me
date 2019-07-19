from pynput.mouse import Button, Controller
from pynput import mouse, keyboard

import time
import tkinter as tk

controller = Controller()

recordings = []

is_recording = False

top = tk.Tk()


def handle_keyboard_event(key):
    global is_recording
    global recordings

    try:
        recordings[int(key.char) - 1].play()
    except Exception as e:
        print("No recording set to key {0}".format(key.char))


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


button = tk.Button(top, text="Record", command=handle_recording)
button.pack()

keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

top.mainloop()
