from tkinter import *

from gui_helpers import run


def build(root):
    choice = IntVar()
    r1 = Radiobutton(root, text="Male", value=1, variable=choice)
    r2 = Radiobutton(root, text="Female", value=2, variable=choice)
    r1.pack()
    r2.pack()

    def show():
        print(choice.get())

    Button(root, text="Message Box", command=show).pack()


if __name__ == "__main__":
    run(build, title="Radiobutton demo", geometry="300x200+300+200")
