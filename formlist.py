from tkinter import *

from gui_helpers import run


def build(root):
    listbox = Listbox(root, width=50, selectmode=EXTENDED)
    listbox.insert(1, "apple")
    listbox.insert(2, "orange")
    listbox.insert(3, "orange")
    listbox.insert(4, "orange")
    listbox.pack()

    def display():
        selected = listbox.curselection()
        print(selected)
        for item in selected:
            print(listbox.get(item))

    def delete():
        for item in listbox.curselection():
            print(listbox.delete(item))

    Button(root, text="Display", command=display).pack()
    Button(root, text="Delete", command=delete).pack()


if __name__ == "__main__":
    run(build, title="Listbox demo", geometry="500x500+300+200")
