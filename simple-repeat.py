from pynput.mouse import Button, Controller as MouseController
from pynput import mouse, keyboard

import time


is_recording = False
recording = []


mouse_controller = MouseController()


def handle_keyboard_event(key):
    global is_recording
    global recording
    global mouse_controller

    if key.char == "r":  # Start/Stop Recordingrp
        is_recording = not is_recording
        if is_recording:  # Start new recording
            print("Recording Started")
            recording = []
        else:
            print("Recording Stopped")

    if key.char == "p":  # Play action back
        for action in recording:
            mouse_controller.position = (action[0], action[1])
            mouse_controller.click(Button.left, 1)
            time.sleep(.5)


def handle_mouse_event(x, y, button, pressed):
    global is_recording
    global recording

    if is_recording:
        if pressed:
            recording.append([x, y])


mouse_listener = mouse.Listener(on_click=handle_mouse_event)
keyboard_listener = keyboard.Listener(on_press=handle_keyboard_event)

keyboard_listener.start()
mouse_listener.start()

while(1 > 0):
    continue
