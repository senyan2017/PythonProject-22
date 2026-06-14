"""combo.py – LabelFrame containing Spinbox and Scale widgets.

Demonstrates: LabelFrame as a visual grouping container, Spinbox
for bounded numeric input, and Scale for slider-based input.
"""
from tkinter import Button, LabelFrame, Spinbox, Scale, HORIZONTAL
from tkhelper import create_window, run


class SpinScaleDemo:
    def __init__(self, root):
        frame = LabelFrame(root, text="Label frame", padx=15, pady=15)

        self.spin = Spinbox(frame, from_=1, to=12)
        self.spin.pack()

        self.scale = Scale(frame, from_=0, to=100, orient=HORIZONTAL,
                           length=200, width=10, sliderlength=50)
        self.scale.set(10)
        self.scale.pack()

        Button(frame, text="Get spin Box value",
               command=self.show_values).pack()

        frame.pack()

    def show_values(self):
        print(self.spin.get())
        print(self.scale.get())


if __name__ == "__main__":
    root = create_window("Spinbox & Scale Demo")
    SpinScaleDemo(root)
    run(root)
