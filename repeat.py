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
        print("adding action")

    def play(self):
        for action in self.actions:
            do_action(action)
            print("Taking action")


def do_action(action):
    controller.position = (action[0], action[1])
    controller.click(Button.left, 1)


def on_click(recording):
    recording.add_action()


def start_recording():
    global recordings
    global listener
    r = Recording()
    recordings.append(r)
    listener = mouse.Listener(on_click=on_click(r))
    listener.start()


def stop_recording():
    global listener
    listener.stop()

    for recording in recordings:
        recording.play()


def handle_recording():
    global is_recording
    if is_recording:
        stop_recording()
        is_recording = False
    else:
        start_recording()
        is_recording = True


button = tk.Button(top, text="Record", command=handle_recording)
button.pack()

top.mainloop()
