"""fontexp.py – Text widget with font styling and search demo.

Demonstrates: Text widget with custom font, insert(), get(),
delete(), selection_get(), and search().
"""
from tkinter import Button, Label, Text, INSERT, END, WORD, font
from tkhelper import create_window, run


class TextDemo:
    def __init__(self, root):
        # Print available font families (educational output).
        for family in font.families():
            print(family)

        Label(root, text="Enter User Name",
              font=("Comic Sans Ms", 20, "bold")).pack()

        self.text = Text(root, width=20, height=10, wrap=WORD,
                         padx=10, pady=10, bd=15,
                         selectbackground="red")
        self.text.insert(INSERT, "Hello")
        self.text.pack()

        Button(root, text="Display",         command=self.show_all).pack()
        Button(root, text="Clear",           command=self.clear).pack()
        Button(root, text="Selected display", command=self.show_selection).pack()
        Button(root, text="Search",          command=self.search_selection).pack()

    def show_all(self):
        print(self.text.get("1.0", END))

    def clear(self):
        self.text.delete("1.0", END)

    def show_selection(self):
        print(self.text.selection_get())

    def search_selection(self):
        needle = self.text.selection_get()
        pos = self.text.search(needle, "1.0", stopindex=END)
        print(pos)


if __name__ == "__main__":
    root = create_window("Text Widget Demo", "500x500+300+200")
    TextDemo(root)
    run(root)
