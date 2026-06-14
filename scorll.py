"""scorll.py – Scrollbar + Listbox demo.

Demonstrates: Scrollbar linked to a Listbox via yscrollcommand,
with Display and Delete action buttons.
"""
from tkinter import Listbox, Button, Frame, Scrollbar, RIGHT, LEFT, Y, END
from tkhelper import create_window, run


class ScrollListDemo:
    def __init__(self, root):
        frame = Frame(root)
        frame.pack()

        self.scrollbar = Scrollbar(frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(frame, width=50, selectmode="extended",
                               yscrollcommand=self.scrollbar.set)
        for i in range(1, 100):
            self.listbox.insert(END, "Element" + str(i))
        self.listbox.pack(side=LEFT)

        self.scrollbar.config(command=self.listbox.yview)

        Button(root, text="Display", command=self.show_selected).pack()
        Button(root, text="Delete",  command=self.delete_selected).pack()

    def show_selected(self):
        for idx in self.listbox.curselection():
            print(self.listbox.get(idx))

    def delete_selected(self):
        for idx in self.listbox.curselection():
            self.listbox.delete(idx)


if __name__ == "__main__":
    root = create_window("Scrollbar Demo", "500x500+300+200")
    ScrollListDemo(root)
    run(root)
