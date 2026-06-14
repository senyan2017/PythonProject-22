"""spinbox.py – Spinbox demo.

Demonstrates: Spinbox widget for bounded numeric input.
"""
from tkinter import Button, Spinbox
from tkhelper import create_window, run


class SpinboxDemo:
    def __init__(self, root):
        self.spin = Spinbox(root, from_=1, to=12)
        self.spin.pack()

        Button(root, text="Get spin Box value",
               command=self.show_value).pack()

    def show_value(self):
        print(self.spin.get())


if __name__ == "__main__":
    root = create_window("Spinbox Demo")
    SpinboxDemo(root)
    run(root)
