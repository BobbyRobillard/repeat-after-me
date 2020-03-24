from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput import mouse, keyboard

import time
import requests

running = True


def handle_keyboard_event(key):
    global running

    # Stop program
    if key.char == "s":
        running = False
        keyboard_listener.stop()
        mouse_listener.stop()

    # Playback recording
    else:
        response = requests.get(
            "http://localhost:8000/play-recording/{0}".format(key.char)
        )
        print(response.status_code)


def handle_mouse_event(x, y, button, pressed):
    print("Mouse Clicked at X: {0}, Y: {1}".format(str(x), str(y)))


mouse_controller = MouseController()
keyboard_controller = KeyboardController()

keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)
mouse_listener = mouse.Listener(on_click=handle_mouse_event)

keyboard_listener.start()
mouse_listener.start()

while running:
    pass
