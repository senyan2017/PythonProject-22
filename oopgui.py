"""oopgui.py – Object-oriented GUI example.

Demonstrates: wrapping widget creation inside a class with
instance methods as callbacks.
"""
from tkinter import Button, LEFT
from tkhelper import create_window, run


class MyForm:
    def __init__(self, root):
        self.print_button = Button(root, text="Message Box",
                                   command=self.on_print)
        self.print_button.pack(side=LEFT)

        self.quit_button = Button(root, text="Exit", command=root.quit)
        self.quit_button.pack(side=LEFT)

    def on_print(self):
        print("Gui form Created")


if __name__ == "__main__":
    root = create_window("OOP GUI Demo")
    MyForm(root)
    run(root)
