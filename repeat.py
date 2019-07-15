from pynput.mouse import Button, Controller
from pynput import mouse

import tkinter as tk

from tkinter import messagebox


# top = tk.Tk()
#
# action = []
#
# controller = Controller()
#
#
# def get_mouse_location():
#     return controller.position
#
#
# def add_mouse_location():
#     action.append(get_mouse_location())
#
#
# def on_click(x, y, button, pressed):
#     add_mouse_location()
#
#
# def take_action():
#     for move in action:
#         controller.position = (move[0], move[1])
#         controller.click(Button.left, 1)
#
#
# listener = mouse.Listener(on_click=on_click)
# listener.start()
#
# button = tk.Button(top, text="Hello", command=take_action)
# button.pack()
#
# top.mainloop()
