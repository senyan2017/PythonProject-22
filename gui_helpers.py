"""Shared helpers for the small Tkinter example scripts in this folder.

The examples used to create their own root window and call ``mainloop`` at
module top level, which meant simply importing one of them popped open a GUI.
These two helpers keep the boilerplate (root creation, default geometry and the
event loop) in one place so each example can focus on the widgets it teaches.

Importing this module never opens a window: ``run`` only starts the event loop,
and examples call it from an ``if __name__ == "__main__"`` block.
"""

import tkinter as tk

DEFAULT_GEOMETRY = "300x200+300+200"


def make_root(title="Tkinter demo", geometry=DEFAULT_GEOMETRY):
    """Create and configure a Tk root window (title + geometry)."""
    root = tk.Tk()
    root.title(title)
    root.geometry(geometry)
    return root


def run(build, title="Tkinter demo", geometry=DEFAULT_GEOMETRY):
    """Build a demo window with ``build(root)`` and run the event loop.

    ``build`` is a callable that receives the root window and adds widgets to
    it. Call this only from an ``if __name__ == "__main__"`` block so that
    importing an example never opens a window.
    """
    root = make_root(title, geometry)
    build(root)
    root.mainloop()
    return root
