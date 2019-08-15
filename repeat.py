from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput import mouse, keyboard

import time
import tkinter as tk

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

recordings = []

playback_mode_active = False
is_recording = False

setting_recording_key = False
setting_playback_key = False

playback_key = None
recording_key = None

top = tk.Tk()

output_text = tk.StringVar()
output = tk.Label(top, textvariable=output_text)
output.config(bg='white', padx=25, pady=25)


def handle_keyboard_event(key):
    global is_playing
    global is_recording

    global recordings

    global setting_recording_key
    global setting_playback_key

    global recording_key
    global playback_key

    global output_text

    try:
        if setting_recording_key:
            recording_key = key.char
            setting_recording_key = False
            output_text.set("Recording key set to: {0}".format(recording_key))

        elif setting_playback_key:
            playback_key = key.char
            setting_playback_key = False
            output_text.set("Playback mode key set to: {0}".format(playback_key))

        elif key.char == playback_key:
            handle_playback()

        else:
            if playback_mode_active:

                if key.char == recording_key:
                    handle_recording()

                elif is_recording:
                    recordings[len(recordings) - 1].actions.append(KeyboardAction(key.char))

                else:
                    play_recording_from_keybind(key.char)

    except AttributeError:
        output_text.set("Special key: {0} pressed".format(key))


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
            time.sleep(0.1)


def handle_recording():
    global is_recording
    global output_text

    is_recording = not is_recording

    if is_recording:
        recordings.append(Recording())
        output_text.set("Recording Started")
    else:
        output_text.set("Recording Stopped")
    # top.update_idletasks()


def handle_playback():
    global playback_mode_active
    global output_text

    playback_mode_active = not playback_mode_active

    if playback_mode_active:
        output_text.set("Playback mode active")
    else:
        output_text.set("Playback mode disabled")


def play_recording_from_keybind(char):
    global keyboard_listener
    global output_text

    keyboard_listener.stop()
    try:
        recordings[int(char) - 1].play()
    except Exception as e:
        output_text.set("No recording set to key {0}".format(char))
    keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
    keyboard_listener.start()


def set_recording_key():
    global setting_recording_key
    global output_text

    setting_recording_key = True
    output_text.set("Please enter the key to start/stop recording...\n")


def set_playback_key():
    global setting_playback_key
    global output_text

    setting_playback_key = True
    output_text.set("Please enter the key to start/stop playback mode...\n")


def delete_recordings():
    global output_text
    global recordings

    output_text.set("Recordings deleted\n")
    recordings = []


record_button = tk.Button(top, text="Set Recording Key", command=set_recording_key)
playback_button = tk.Button(top, text="Set Playback Key", command=set_playback_key)
delete_recordings_button = tk.Button(top, text="Delete Recordings", command=delete_recordings)

record_button.pack()
playback_button.pack()
delete_recordings_button.pack()
output.pack()

keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

top.mainloop()
