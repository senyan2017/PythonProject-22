"""guiplace.py – Labels positioned with place() layout.

Demonstrates: Frame and Label using the place geometry manager
for absolute x/y positioning.
"""
from tkinter import Label, Frame
from tkhelper import create_window, run


def build_ui(root):
    """Place two labels at fixed coordinates inside a frame."""
    frame = Frame(root, width=400, height=400)

    Label(frame, text="Enter User Name").place(x=10, y=10)
    Label(frame, text="Enter User Password").place(x=10, y=40)

    frame.pack()


if __name__ == "__main__":
    root = create_window("Place Layout")
    build_ui(root)
    run(root)
