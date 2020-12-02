from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from pynput import mouse, keyboard

from operator import attrgetter

import requests
import time
import json

import atexit


default_username = "webmaster"
domain = "http://localhost:8000"
token = "45ce395dc6aa1761ddf3c9ebf0c0454190fd4736"

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

actions = []

playback_mode_active = False
is_recording = False

playback_key = "Key.tab"
recording_key = "r"


def handle_keyboard_event(key):
    global actions
    global is_recording

    global recording_key
    global playback_key

    try:  # Normal Key Pressed
        if key.char == playback_key:
            handle_playback()
        elif playback_mode_active:
            if key.char == recording_key:
                handle_recording()
            elif is_recording:
                # TODO: This needs to store more info on press / release
                actions.append(KeyboardAction(key.char))
            else:
                play_recording(key.char)

    except AttributeError:  # Special Key Pressed
        key = str(key)
        if key == playback_key:
            handle_playback()
        elif playback_mode_active:
            if key == recording_key:
                handle_recording()
            elif is_recording:
                # TODO: This needs to store more info on press / release
                actions.append(KeyboardAction(key))
            else:
                play_recording(key)


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
        return "KA: {0}".format(self.char)

    def do_action(self):
        global keyboard_controller
        keyboard_controller.type(self.char)


def handle_recording():
    global is_recording
    global actions
    is_recording = not is_recording
    print("Recording: {0}".format(str(is_recording)))

    if is_recording:
        # Tell server a recording has started
        response = requests.get("{0}/macros/start-recording/{1}".format(domain, token))
    else:
        # Stop recording and upload recording to server
        upload_recording()


def handle_playback():
    global playback_mode_active
    playback_mode_active = not playback_mode_active
    print("Playback: {0}".format(str(playback_mode_active)))

    if playback_mode_active:
        # Tell server to toggle play mode is active
        response = requests.get(
            "{0}/macros/toggle-play-mode/{1}/{2}/".format(domain, token, str(1))
        )
    else:
        # Tell server to toggle play mode is inactive
        response = requests.get(
            "{0}/macros/toggle-play-mode/{1}/{2}/".format(domain, token, str(0))
        )


# TODO: There needs to be a way for a "fail-safe" stop
def play_recording(char):
    global keyboard_listener

    keyboard_listener.stop()

    try:
        response = requests.get(
            "{0}/macros/download-recording/{1}/{2}".format(domain, token, char)
        )

        json_data = json.loads(response.text)["events"]

        events = sorted(json_data, key=lambda i: i["order_in_recording"])

        for event in events:
            print(event)
            try:
                mouse_controller.position = (event["x_pos"], event["y_pos"])
                mouse_controller.click(Button.left)
            except Exception as e:
                key_code = event["key_code"]
                if len(key_code) == 1:
                    keyboard_controller.type(key_code)
                else:
                    keyboard_controller.press(eval(key_code))
                    keyboard_controller.release(eval(key_code))
            time.sleep(.05)
    except Exception as e:
        print(str(e))
    keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
    keyboard_listener.start()


def delete_recording():
    global actions
    actions = []


def upload_recording():
    global actions

    if len(actions) > 0:
        key_events = []
        mouse_events = []

        order_in_recording = 0

        print("Uploading Recording")
        # Json format
        for action in actions:
            if type(action) is KeyboardAction:
                key_events.append(
                    {
                        "key_code": action.char,
                        "delay_time": 0,
                        "order_in_recording": order_in_recording,
                        "is_press": True,
                    }
                )
            else:
                mouse_events.append(
                    {
                        "x_pos": action.x,
                        "y_pos": action.y,
                        "delay_time": 0,
                        "is_press": True,
                        "button": str(action.button),
                        "order_in_recording": order_in_recording,
                    }
                )

            order_in_recording = order_in_recording + 1

        url = "{0}/macros/stop-recording/{1}/".format(domain, token)
        requests.post(
            url, json={"key_events": key_events, "mouse_events": mouse_events}
        )
        actions = []
        print("Upload Complete")


# Sync settings with server
def sync():
    print("Syncing With Server")
    response = requests.get("{0}/macros/sync/{1}/".format(domain, token))
    print("Synced!")


# --------------------------------------------------------------------------


# print("Setup Started")
keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

sync()
print("Starting App")

# Sync settings with server when application is close
atexit.register(sync)


while True:
    pass
