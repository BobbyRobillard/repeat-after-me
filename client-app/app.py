from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput import mouse, keyboard

import requests
import time
import json

default_username = "webmaster"
domain = "http://localhost:8000"

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

actions = []

playback_mode_active = False
is_recording = False

playback_key = "p"
recording_key = "r"


def handle_keyboard_event(key):
    global actions
    global is_recording

    global recording_key
    global playback_key

    try:
        if key.char == playback_key:
            handle_playback()

        else:
            if playback_mode_active:
                if key.char == recording_key:
                    handle_recording()

                elif is_recording:
                    # TODO: This needs to store more info on press / release
                    actions.append(KeyboardAction(key.char))

                else:
                    # play_recording(key.char)
                    pass

    except AttributeError:
        print("Special key: {0} pressed".format(key))


def handle_mouse_event(x, y, button, pressed):
    global recordings
    global is_recording

    if is_recording:
        if pressed:
            actions.append(MouseAction(x, y, button))


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


def handle_recording():
    global is_recording
    global actions
    is_recording = not is_recording
    print("Recording: {0}".format(str(is_recording)))

    if is_recording:
        # Tell server a recording has started
        response = requests.get(
            "http://localhost:8000/macros/toggle-recording/{0}/{1}".format(
                default_username, str(1)
            )
        )
    else:
        # Tell server a recording has stopped
        response = requests.get(
            "http://localhost:8000/macros/toggle-recording/{0}/{1}".format(
                default_username, str(0)
            )
        )
        # Upload recording to server
        upload_recording()


def handle_playback():
    global playback_mode_active
    playback_mode_active = not playback_mode_active
    print("Playback: {0}".format(str(playback_mode_active)))

    if playback_mode_active:
        # Tell server to toggle play mode is active
        response = requests.get(
            "http://localhost:8000/macros/toggle-play-mode/{0}/{1}".format(
                default_username, str(1)
            )
        )
    else:
        # Tell server to toggle play mode is inactive
        response = requests.get(
            "http://localhost:8000/macros/toggle-play-mode/{0}/{1}".format(
                default_username, str(0)
            )
        )


# TODO: There needs to be a way for a "fail-safe" stop
def play_recording(char):
    global keyboard_listener

    keyboard_listener.stop()

    try:
        print("Playing recording")

    except Exception as e:
        output_text.set("No recording set to key {0}".format(char))

    keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
    keyboard_listener.start()


def delete_recording():
    global actions
    actions = []


def upload_recording():
    global actions
    print("Uploading Recording")
    url = "{0}/macros/upload-recording/{1}".format(domain, default_username)

    # Json format
    for action in actions:
        if type(action) is KeyboardAction:
            requests.post(url, json={"key": str(action.char)})
        else:
            formatted_action = {
                "x": action.x,
                "y": action.y,
                "button": str(action.button),
            }
            requests.post(url, json=json.dumps(formatted_action))


# --------------------------------------------------------------------------

keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

while True:
    pass
