"""Graphical.py – Mouse-button event binding demo.

Demonstrates: Button.bind() for <Button-1>, <Button-2>, <Button-3>
events, and mixing multiple frames with pack().
"""
from tkinter import Button, Entry, Frame
from tkhelper import create_window, run


def on_left_click(event):
    print("Left button is clicked")


def on_middle_click(event):
    print("Middle button is clicked")


def on_right_click(event):
    print("right button is clicked")


def build_ui(root):
    # --- top frame: three event-bound buttons ---
    top = Frame(root)

    btn_left = Button(top, text="Left Click", bg="red", fg="white")
    btn_left.bind("<Button-1>", on_left_click)
    btn_left.pack(side="left")

    btn_middle = Button(top, text="Middle click")
    btn_middle.bind("<Button-2>", on_middle_click)
    btn_middle.pack(side="left")

    btn_right = Button(top, text="Right Click")
    btn_right.bind("<Button-3>", on_right_click)
    btn_right.pack(side="left")

    top.pack()

    # --- bottom frame: entry + fill-width button ---
    bottom = Frame(root)
    Entry(bottom).pack()
    Button(bottom, text="Button4", bg="yellow").pack(fill="x")
    bottom.pack(side="bottom")


if __name__ == "__main__":
    root = create_window("Event Binding Demo")
    build_ui(root)
    run(root)
