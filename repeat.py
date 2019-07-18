from pynput.mouse import Button, Controller
from pynput import mouse

import tkinter as tk

import sys

controller = Controller()

recordings = []

is_recording = False


def on_click(x, y, button, pressed):
    print("Click Started")
    global recordings
    if pressed:
        recordings[len(recordings) - 1].add_action()
        print("Press Succeeded")
    else:
        print("Release Succeeded")


listener = mouse.Listener(on_click=on_click)

top = tk.Tk()


class Recording:
    def __init__(self):
        self.actions = []
        self.key_bind_code = -1

    def add_action(self):
        print("Add action started")
        global controller
        self.actions.append(controller.position)
        print("Add action Succeeded")

    def play(self):
        for action in self.actions:
            do_action(action)


def do_action(action):
    controller.position = (action[0], action[1])
    controller.click(Button.left, 1)


def start_recording():
    print("Recording Started")
    global recordings
    global listener
    recordings.append(Recording())
    listener = mouse.Listener(on_click=on_click)
    listener.start()


def stop_recording():
    print("Recording Stopped")
    global listener
    listener.stop()

    for recording in recordings:
        for action in recording.actions:
            print(str(action))


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
