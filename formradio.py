"""formradio.py – RadioButton demo.

Demonstrates: IntVar-bound RadioButton group and reading the
selected value on a button click.
"""
from tkinter import IntVar, Radiobutton, Button
from tkhelper import create_window, run


class RadioDemo:
    def __init__(self, root):
        self.choice = IntVar()

        Radiobutton(root, text="Male",   value=1, variable=self.choice).pack()
        Radiobutton(root, text="Female", value=2, variable=self.choice).pack()

        Button(root, text="Message Box", command=self.show_choice).pack()

    def show_choice(self):
        print(self.choice.get())


if __name__ == "__main__":
    root = create_window("RadioButton Demo")
    RadioDemo(root)
    run(root)
