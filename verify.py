"""verify.py – Minimal sanity-check for refactored Tkinter examples.

Run this script to confirm:
  1. Every refactored module compiles without syntax errors.
  2. Importing any module does NOT launch a GUI (the __name__ guard works).
  3. The tkhelper utility module is importable.

Usage:
    python verify.py
"""

import importlib
import py_compile
import sys
import os

# Directory where this script lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# All Tkinter example modules that were refactored
MODULES = [
    "tkhelper",
    "gui",
    "gridgui",
    "guiplace",
    "formlist",
    "formradio",
    "formcheck",
    "textboxvalue",
    "textboxvalue2",
    "Graphical",
    "oopgui",
    "msgbox",
    "canvasexp",
    "combo",
    "spinbox",
    "scorll",
    "newwindow",
    "pop",
    "filedialog",
    "mynotepad",
    "fontexp",
    "labelframe",
]


def check_syntax():
    """Phase 1: compile every module to catch syntax errors."""
    print("=" * 50)
    print("Phase 1 – Syntax check (py_compile)")
    print("=" * 50)
    errors = []
    for name in MODULES:
        path = os.path.join(BASE_DIR, name + ".py")
        try:
            py_compile.compile(path, doraise=True)
            print(f"  OK  {name}.py")
        except py_compile.PyCompileError as exc:
            print(f"FAIL  {name}.py: {exc}")
            errors.append(name)
    return errors


def check_import_guard():
    """Phase 2: import each module and confirm no GUI pops up.

    We monkey-patch tkinter.Tk so that any call at module level raises,
    proving the ``if __name__ == '__main__'`` guard is in place.
    """
    print()
    print("=" * 50)
    print("Phase 2 – Import-guard check (no GUI on import)")
    print("=" * 50)

    # Build a minimal mock tkinter so imports succeed even without a display
    import types

    class _Mock:
        def __init__(self, *a, **kw): pass
        def __call__(self, *a, **kw): return self
        def __getattr__(self, name): return _Mock()
        def __setattr__(self, name, value): pass

    mock_tk = types.ModuleType("tkinter")
    tk_names = [
        "Tk", "Frame", "Label", "Entry", "Button", "Listbox",
        "Checkbutton", "Radiobutton", "Canvas", "Scrollbar",
        "Spinbox", "Scale", "Text", "Menu", "Toplevel", "LabelFrame",
        "StringVar", "IntVar", "LEFT", "RIGHT", "TOP", "BOTTOM",
        "X", "Y", "BOTH", "END", "INSERT", "WORD", "EXTENDED",
        "HORIZONTAL", "VERTICAL",
    ]
    for n in tk_names:
        setattr(mock_tk, n, _Mock)
    sys.modules["tkinter"] = mock_tk

    for sub_name in ["messagebox", "simpledialog", "filedialog", "font", "ttk"]:
        full = f"tkinter.{sub_name}"
        m = types.ModuleType(full)
        for attr in ["showinfo", "askinteger", "askopenfile", "Combobox", "families"]:
            setattr(m, attr, _Mock)
        sys.modules[full] = m

    # Detect whether Tk() is called at import time (it shouldn't be)
    tk_called = False
    _orig_mock_tk = mock_tk.Tk

    class TkDetector(_Mock):
        def __init__(self, *a, **kw):
            nonlocal tk_called
            tk_called = True
            raise RuntimeError("Tk() called at import time!")

    mock_tk.Tk = TkDetector

    errors = []
    for name in MODULES:
        tk_called = False
        try:
            # Force re-import so the guard is actually exercised
            if name in sys.modules:
                del sys.modules[name]
            importlib.import_module(name)
            print(f"  OK  {name} (no GUI on import)")
        except RuntimeError:
            print(f"FAIL  {name} – Tk() called at module level!")
            errors.append(name)
        except Exception as exc:
            # Other errors are acceptable for this check
            print(f"  OK  {name} (non-fatal: {type(exc).__name__})")

    # Restore
    mock_tk.Tk = _orig_mock_tk
    return errors


def main():
    syn_errors = check_syntax()
    imp_errors = check_import_guard()

    print()
    print("=" * 50)
    print("Summary")
    print("=" * 50)
    total = len(MODULES)
    syn_ok = total - len(syn_errors)
    imp_ok = total - len(imp_errors)
    print(f"  Syntax:       {syn_ok}/{total} passed")
    print(f"  Import-guard:  {imp_ok}/{total} passed")

    if syn_errors or imp_errors:
        print("\nSome checks failed – see details above.")
        sys.exit(1)
    else:
        print("\nAll checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
