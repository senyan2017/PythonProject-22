"""Minimal functional check for mynotepad.py.

It drives the real editor methods but monkeypatches the file dialogs and
message boxes, so it runs without any clicking and without popups. It needs
tkinter (Debian/Ubuntu: `sudo apt install python3-tk`) and a display; if
either is missing it prints SKIP and exits 0.

Run:  python3 test_mynotepad.py
"""
import os
import shutil
import sys
import tempfile


def main():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception as e:                       # tkinter not installed
        print("SKIP: tkinter not available ({}). "
              "Install python3-tk to run GUI tests.".format(e))
        return 0
    try:
        root = tk.Tk()
        root.withdraw()                          # keep the window hidden
    except Exception as e:                        # no usable display
        print("SKIP: no usable display ({}).".format(e))
        return 0

    import mynotepad
    ed = mynotepad.text_editor(root)

    failures = []

    def check(cond, msg):
        print(("PASS: " if cond else "FAIL: ") + msg)
        if not cond:
            failures.append(msg)

    tmpdir = tempfile.mkdtemp()
    p1 = os.path.join(tmpdir, "note1.txt")
    p2 = os.path.join(tmpdir, "note2.txt")
    try:
        # 1) type something + first Save (no current file -> Save As flow)
        ed.text_area.insert("1.0", "hello\nworld")
        check(ed.text_area.edit_modified(), "editing marks the buffer modified")
        filedialog.asksaveasfilename = lambda *a, **k: p1
        ok = ed.save_file()
        check(ok and os.path.exists(p1), "first Save writes a new file")
        with open(p1, encoding="utf-8") as f:
            check(f.read() == "hello\nworld", "saved content round-trips exactly")
        check(not ed.text_area.edit_modified(), "Save clears the modified flag")
        check(ed.current_file == p1, "current file is tracked after Save")

        # 2) overwrite the existing file (Save reuses the path, no dialog)
        ed.text_area.insert("end", "\nmore")
        ok = ed.save_file()
        with open(p1, encoding="utf-8") as f:
            check(ok and f.read() == "hello\nworld\nmore",
                  "Save overwrites the current file")

        # 3) Save As to a different path
        filedialog.asksaveasfilename = lambda *a, **k: p2
        ok = ed.save_as_file()
        check(ok and os.path.exists(p2) and ed.current_file == p2,
              "Save As switches to the new path")

        # 4) cancelling Save As returns False and changes nothing
        filedialog.asksaveasfilename = lambda *a, **k: ""
        keep = ed.current_file
        ok = ed.save_as_file()
        check(ok is False and ed.current_file == keep,
              "cancelled Save As is a no-op")

        # 5) Open loads file content into the editor
        messagebox.askyesnocancel = lambda *a, **k: False   # discard if prompted
        filedialog.askopenfilename = lambda *a, **k: p1
        ed.open_file()
        check(ed.text_area.get("1.0", "end-1c") == "hello\nworld\nmore",
              "Open loads file content into the editor")
        check(ed.current_file == p1 and not ed.text_area.edit_modified(),
              "Open updates the path and clears modified")

        # 6) cancelling Open leaves the editor untouched
        before = ed.text_area.get("1.0", "end-1c")
        filedialog.askopenfilename = lambda *a, **k: ""
        ed.open_file()
        check(ed.text_area.get("1.0", "end-1c") == before,
              "cancelled Open leaves the editor unchanged")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        root.destroy()

    if failures:
        print("\n{} check(s) failed".format(len(failures)))
        return 1
    print("\nALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
