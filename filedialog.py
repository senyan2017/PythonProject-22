"""filedialog.py – File-open dialog demo.

Demonstrates: filedialog.askopenfile() for selecting and reading
a file chosen through a native OS dialog.
"""
from tkinter import Button
from tkinter import filedialog
from tkhelper import create_window, run


def open_file():
    f = filedialog.askopenfile(
        initialdir="c://",
        title="Select file",
        filetypes=(("text file", "*.txt"), ("all files", "*.*")),
    )
    if f is not None:
        for line in f:
            print(line)


def build_ui(root):
    Button(root, text="Open File", command=open_file).pack()


if __name__ == "__main__":
    root = create_window("File Dialog Demo")
    build_ui(root)
    run(root)
