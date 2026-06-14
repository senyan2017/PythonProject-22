from tkinter import *

from gui_helpers import run


def build(root):
    def msg():
        print("button is clicked")

    frame = Frame(root, width=400, height=400)
    user = Label(frame, text="Enter User Name")
    user.grid(row=0)
    pas = Label(frame, text="Enter User Password")
    pas.grid(row=1, column=0)

    entry = Entry(frame)
    entry.grid(row=0, column=1)
    entry1 = Entry(frame)
    entry1.grid(row=1, column=1)
    button1 = Button(frame, text="Login and Save", bg="red", fg="white", command=msg)
    button1.grid(columnspan=2)
    frame.pack()


if __name__ == "__main__":
    run(build, title="Login form (grid)", geometry="300x200+300+200")
