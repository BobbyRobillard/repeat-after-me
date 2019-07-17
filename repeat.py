from pynput.mouse import Button, Controller
from pynput import mouse

import tkinter as tk

import sys

controller = Controller()

recordings = []

is_recording = False

listener = None

top = tk.Tk()


class Recording:
    def __init__(self):
        self.actions = []
        self.key_bind_code = -1

    def add_action(self):
        self.actions.append(controller.position)

    def play(self):
        for action in actions:
            do_action(action)


def do_action(action):
    controller.position = (action[0], action[1])
    controller.click(Button.left, 1)


def on_click(recording):
    recording.add_action()
    print("Action added")


def start_recording():
    r = Recording()
    recordings.append(r)
    listener = mouse.Listener(on_click=on_click(r))
    listener.start()
    print("Recording Started")
    print("Recording: " + str(is_recording))


def stop_recording():
    listener.stop()
    print("Recording Stopped")
    print(str(recordings[len(recordings) - 1]))


def handle_recording():
    print("Recording: " + str(is_recording))
    if is_recording:
        stop_recording()
        is_recording = False
    else:
        start_recording()
        is_recording = True


button = tk.Button(top, text="Record", command=handle_recording)
button.pack()

top.mainloop()
