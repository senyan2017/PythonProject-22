"""pop.py – Simple-dialog (prompt) demo.

Demonstrates: simpledialog.askinteger() for getting numeric input
from the user via a modal dialog.
"""
from tkinter import Button
from tkinter import simpledialog
from tkhelper import create_window, run


def ask_integer():
    value = simpledialog.askinteger("Input Box", "Please Enter a number")
    print(type(value), value)


def build_ui(root):
    Button(root, text="Prompt Box", command=ask_integer).pack()


if __name__ == "__main__":
    root = create_window("Prompt Dialog Demo")
    build_ui(root)
    run(root)
