"""formcheck.py – Checkbutton demo.

Demonstrates: StringVar-bound Checkbutton with onvalue/offvalue
and reading the state on a button click.
"""
from tkinter import StringVar, Checkbutton, Button
from tkhelper import create_window, run


class CheckDemo:
    def __init__(self, root):
        self.hindi_var = StringVar()

        Checkbutton(root, text="Hindi", variable=self.hindi_var,
                    offvalue="unchecked", onvalue="checked").pack()

        Button(root, text="Message Box", command=self.show_value).pack()

    def show_value(self):
        print(self.hindi_var.get())


if __name__ == "__main__":
    root = create_window("Checkbutton Demo")
    CheckDemo(root)
    run(root)
