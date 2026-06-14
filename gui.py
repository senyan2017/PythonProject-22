from tkinter import *

from gui_helpers import run


def build(root):
    user_name = Label(root, text="Enter User Name", bg="black", fg="white")
    user_name.pack(side=LEFT)
    entry = Entry(root, bg="black", fg="white")
    entry.pack(side=LEFT)
    btn = Button(root, text="Login")
    btn.pack(side=LEFT)


if __name__ == "__main__":
    run(build, title="Login", geometry="300x200+200+300")
