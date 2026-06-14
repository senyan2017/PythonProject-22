"""formlist.py – Listbox demo with Display and Delete buttons.

Demonstrates: Listbox widget with EXTENDED selectmode,
curselection(), get(), and delete() methods.
"""
from tkinter import Listbox, Button, EXTENDED, END
from tkhelper import create_window, run


class ListBoxDemo:
    def __init__(self, root):
        self.listbox = Listbox(root, width=50, selectmode=EXTENDED)
        for item in ("apple", "orange", "orange", "orange"):
            self.listbox.insert(END, item)
        self.listbox.pack()

        Button(root, text="Display", command=self.show_selected).pack()
        Button(root, text="Delete",  command=self.delete_selected).pack()

    def show_selected(self):
        for idx in self.listbox.curselection():
            print(self.listbox.get(idx))

    def delete_selected(self):
        for idx in self.listbox.curselection():
            self.listbox.delete(idx)


if __name__ == "__main__":
    root = create_window("Listbox Demo", "500x500+300+200")
    ListBoxDemo(root)
    run(root)
