"""canvasexp.py – Canvas drawing demo.

Demonstrates: Canvas widget with create_line, create_rectangle,
create_oval, create_arc, and create_polygon.
"""
from tkinter import Canvas
from tkhelper import create_window, run


def build_ui(root):
    canvas = Canvas(root, width=500, height=500, bg="yellow")
    canvas.pack()

    canvas.create_line(0, 0, 300, 300)
    canvas.create_line(0, 150, 300, 150, fill="red")
    canvas.create_rectangle(100, 100, 200, 200, fill="blue")
    canvas.create_oval(100, 100, 200, 200, fill="red")
    canvas.create_arc(100, 100, 200, 200, extent=120, fill="yellow")

    points = [250, 110, 480, 200, 280, 280, 250, 110]
    canvas.create_polygon(points, fill="white", outline="red", width=5)


if __name__ == "__main__":
    root = create_window("Canvas Demo", "800x800+300+200")
    build_ui(root)
    run(root)
