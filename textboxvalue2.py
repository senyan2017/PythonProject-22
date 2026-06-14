"""textboxvalue2.py – Entry with IntVar demo.

Demonstrates: IntVar bound to an Entry via textvariable for
numeric input, and reading the integer value on a button click.
"""
from tkinter import IntVar, Entry, Button
from tkhelper import create_window, run


class EntryIntDemo:
    def __init__(self, root):
        self.num_var = IntVar()

        entry = Entry(root, textvariable=self.num_var, insertwidth=3)
        entry.pack()

        Button(root, text="Message Box", command=self.show_value).pack()

    def show_value(self):
        print(self.num_var.get())


if __name__ == "__main__":
    root = create_window("Entry IntVar Demo")
    EntryIntDemo(root)
    run(root)
