from pynput.mouse import Button, Controller
from pynput import mouse

import tkinter as tk

controller = Controller()

recordings = []

is_recording = False

top = tk.Tk()


def on_click(x, y, button, pressed):
    print("Click Started")
    global recordings
    global is_recording
    if is_recording:
        if pressed:
            recordings[len(recordings) - 1].add_action()
            print("Press Succeeded")
        else:
            print("Release Succeeded")


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


def handle_recording():
    global is_recording

    if not is_recording:
        recordings.append(Recording())

    is_recording = not is_recording


button = tk.Button(top, text="Record", command=handle_recording)
button.pack()

listener = mouse.Listener(on_click=on_click)
listener.start()
listener.join()
top.mainloop()
