"""textboxvalue.py – Entry with StringVar demo.

Demonstrates: StringVar bound to an Entry via textvariable,
and presetting a default value with .set().
"""
from tkinter import StringVar, Entry, Button
from tkhelper import create_window, run


class EntryStringDemo:
    def __init__(self, root):
        self.text_var = StringVar()
        self.text_var.set("Hello")

        entry = Entry(root, textvariable=self.text_var, insertwidth=3)
        entry.pack()

        Button(root, text="Message Box", command=self.show_value).pack()

    def show_value(self):
        print(self.text_var.get())


if __name__ == "__main__":
    root = create_window("Entry StringVar Demo")
    EntryStringDemo(root)
    run(root)
