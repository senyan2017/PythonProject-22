"""gridgui.py – Login form using grid() layout.

Demonstrates: Label, Entry, Button with grid geometry manager,
including columnspan for spanning the button across columns.
"""
from tkinter import Label, Entry, Button, Frame
from tkhelper import create_window, run


def on_login():
    print("button is clicked")


def build_ui(root):
    """Build a two-row login form with grid layout."""
    frame = Frame(root, width=400, height=400)

    Label(frame, text="Enter User Name").grid(row=0, column=0)
    Label(frame, text="Enter User Password").grid(row=1, column=0)

    Entry(frame).grid(row=0, column=1)
    Entry(frame).grid(row=1, column=1)

    Button(frame, text="Login and Save", bg="red", fg="white",
           command=on_login).grid(columnspan=2)

    frame.pack()


if __name__ == "__main__":
    root = create_window("Grid Login")
    build_ui(root)
    run(root)
