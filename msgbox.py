"""msgbox.py – Messagebox demo.

Demonstrates: messagebox.showinfo() and reacting to the user's
response (yes / ok / cancel, etc.).
"""
from tkinter import Button
from tkinter import messagebox
from tkhelper import create_window, run


def build_ui(root):
    def on_show_message():
        ans = messagebox.showinfo("Question Box", "Do you want to close?")
        print(ans)
        if ans == "yes":
            print("thank you")
        else:
            root.quit()

    Button(root, text="Message Box", command=on_show_message).pack()


if __name__ == "__main__":
    root = create_window("Messagebox Demo")
    build_ui(root)
    run(root)
