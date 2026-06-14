"""labelframe.py – Combobox (ttk) demo.

Demonstrates: ttk.Combobox populated with a value list and
reading the current selection on a button click.
"""
from tkinter import Button, END
from tkinter.ttk import Combobox
from tkhelper import create_window, run


class ComboboxDemo:
    def __init__(self, root):
        cities = ["Gkp", "Ndls", "lko", "1", "4", "666"]

        self.combo = Combobox(root, values=cities)
        self.combo.set("select your city")
        self.combo.pack()

        Button(root, text="Display", command=self.show_value).pack()

    def show_value(self):
        print(self.combo.get())


if __name__ == "__main__":
    root = create_window("Combobox Demo", "500x500+300+200")
    ComboboxDemo(root)
    run(root)
