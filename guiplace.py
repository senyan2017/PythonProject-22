from tkinter import *

from gui_helpers import run


def build(root):
    frame = Frame(root, width=400, height=400)
    user = Label(frame, text="Enter User Name")
    user.place(x=10, y=10)
    pas = Label(frame, text="Enter User Password")
    pas.place(x=10, y=40)
    frame.pack()


if __name__ == "__main__":
    run(build, title="Login form (place)", geometry="300x200+300+200")
