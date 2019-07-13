from pynput.mouse import Button, Controller

import tkinter as tk

from tkinter import messagebox


top = tk.Tk()

def get_mouse_location():
    mouse = Controller()
    msg = messagebox.showinfo(
        "Hello Python",
        "The current pointer position is {0}".format(mouse.position)
    )

button = tk.Button(top, text="Hello", command=get_mouse_location)
button.pack()

top.mainloop()
