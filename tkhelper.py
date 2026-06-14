"""
tkhelper.py - Lightweight helper for Tkinter demo scripts.

Provides common window-creation boilerplate so each example can focus
on the widget it is demonstrating.  Intentionally small: importing this
module should feel like including a single utility function, not a framework.

Usage
-----
    from tkhelper import create_window, run

    root = create_window("My Demo", "400x300")
    # ... build widgets on `root` ...
    run(root)
"""

from tkinter import Tk


# ---------------------------------------------------------------------------
# Sensible defaults – override per-call when an example needs something else.
# ---------------------------------------------------------------------------
DEFAULT_GEOMETRY = "300x200+300+200"


def create_window(title: str = "Demo", geometry: str = DEFAULT_GEOMETRY) -> Tk:
    """Create and return a configured Tk root window.

    Parameters
    ----------
    title : str
        Window title shown in the title bar.
    geometry : str
        Tk geometry string, e.g. ``"400x300+100+100"``.
    """
    root = Tk()
    root.title(title)
    root.geometry(geometry)
    return root


def run(root: Tk) -> None:
    """Enter the Tk event loop for *root*.

    Separated so examples can do any last-minute setup between
    ``create_window`` and ``run`` if needed.
    """
    root.mainloop()
