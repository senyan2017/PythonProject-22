"""gui.py – Simple login form using pack() layout.

Demonstrates: Label, Entry, Button with pack geometry manager.
"""
from tkinter import Label, Entry, Button
from tkhelper import create_window, run


def build_ui(root):
    """Build a minimal label + entry + button row."""
    Label(root, text="Enter User Name", bg="black", fg="white").pack(side="left")
    Entry(root, bg="black", fg="white").pack(side="left")
    Button(root, text="Login").pack(side="left")


if __name__ == "__main__":
    root = create_window("Login Form")
    build_ui(root)
    run(root)
