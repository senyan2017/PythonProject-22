"""newwindow.py – Toplevel child-window demo.

Demonstrates: opening a secondary window with Toplevel() and
closing it independently from the main window.
"""
from tkinter import Button, Toplevel
from tkhelper import create_window, run


def open_child_window():
    child = Toplevel()
    child.title("child window")
    child.geometry("300x200+300+200")
    Button(child, text="close", command=child.destroy).pack()


def build_ui(root):
    root.title("Registration form")
    Button(root, text="Message Box", command=open_child_window).pack()


if __name__ == "__main__":
    root = create_window("Registration form")
    build_ui(root)
    run(root)
