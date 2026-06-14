"""mynotepad.py – Minimal text-editor demo.

Demonstrates: OOP design with Menu, Text widget, and filedialog
for open/save operations.
"""
from tkinter import Menu, Text, BOTH, filedialog
from tkhelper import create_window, run


class TextEditor:
    def __init__(self, root):
        self.root = root
        root.title("MyNotePAd")

        # --- text area ---
        self.text_area = Text(root)
        self.text_area.pack(fill=BOTH, expand=1)

        # --- menu bar ---
        self.main_menu = Menu(root)
        root.config(menu=self.main_menu)

        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open",   command=self.open_file)
        self.file_menu.add_command(label="Save",   command=self.save_file)
        self.file_menu.add_command(label="SaveAs", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        self.main_menu.add_cascade(label="Edit", menu=self.file_menu)

    # ---- file operations ------------------------------------------------
    def open_file(self):
        f = filedialog.askopenfile(
            initialdir="c://",
            title="Select file",
            filetypes=(("text file", "*.txt"), ("all files", "*.*")),
        )
        if f is not None:
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", f.read())

    def save_file(self):
        pass

    def save_as_file(self):
        pass


if __name__ == "__main__":
    root = create_window("MyNotePAd")
    TextEditor(root)
    run(root)
