from tkinter import *

from gui_helpers import run


def build(root):
    state = StringVar()
    c = Checkbutton(root, text="Hindi", variable=state,
                    offvalue="unchecked", onvalue="checked")
    c.pack()

    def show():
        print(state.get())

    Button(root, text="Message Box", command=show).pack()


if __name__ == "__main__":
    run(build, title="Checkbutton demo", geometry="300x200+300+200")
