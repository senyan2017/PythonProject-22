import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class text_editor:

    # ----- low level helpers (no dialogs, easy to test) -----------------
    def _read_into_editor(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.text_area.delete(1.0, END)
        self.text_area.insert(1.0, content)
        self.current_file = path
        self._mark_clean()

    def _write_to_path(self, path):
        # "end-1c" drops the trailing newline Tk adds automatically so the
        # file content round-trips exactly.
        content = self.text_area.get(1.0, "end-1c")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.current_file = path
        self._mark_clean()

    # ----- state / title ------------------------------------------------
    def _mark_clean(self):
        self.text_area.edit_modified(False)
        self._update_title()

    def _on_modified(self, event=None):
        # Fired by the Text widget's <<Modified>> virtual event. We only read
        # the flag here (never set it) so there is no recursion.
        self._update_title()

    def _update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        star = "*" if self.text_area.edit_modified() else ""
        self.master.title("{}{} - MyNotePad".format(star, name))

    def _maybe_save_changes(self):
        """Ask to save when there are unsaved edits.

        Returns True if it is safe to proceed (saved or discarded), False if
        the user cancelled and the pending action should be aborted.
        """
        if not self.text_area.edit_modified():
            return True
        resp = messagebox.askyesnocancel(
            "Unsaved changes",
            "You have unsaved changes. Save before continuing?")
        if resp is None:        # Cancel
            return False
        if resp:                # Yes -> save (False if save dialog cancelled)
            return self.save_file()
        return True             # No -> discard

    # ----- menu actions -------------------------------------------------
    def new_file(self):
        if not self._maybe_save_changes():
            return
        self.text_area.delete(1.0, END)
        self.current_file = None
        self._mark_clean()

    def open_file(self):
        if not self._maybe_save_changes():
            return
        path = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Text file", "*.txt"), ("All files", "*.*")))
        if not path:            # user cancelled
            return
        try:
            self._read_into_editor(path)
        except (OSError, UnicodeDecodeError) as e:
            messagebox.showerror("Open failed", "Could not open file:\n{}".format(e))

    def save_file(self):
        """Save to the current file, or fall back to Save As on first save.

        Returns True if the content was written, False if cancelled.
        """
        if self.current_file:
            try:
                self._write_to_path(self.current_file)
                return True
            except OSError as e:
                messagebox.showerror("Save failed", "Could not save file:\n{}".format(e))
                return False
        return self.save_as_file()

    def save_as_file(self):
        """Prompt for a path and save there. Returns True if written."""
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text file", "*.txt"), ("All files", "*.*")))
        if not path:            # user cancelled
            return False
        try:
            self._write_to_path(path)
            return True
        except OSError as e:
            messagebox.showerror("Save failed", "Could not save file:\n{}".format(e))
            return False

    def select_all(self, event=None):
        self.text_area.tag_add(SEL, "1.0", END)
        self.text_area.mark_set(INSERT, "1.0")
        self.text_area.see(INSERT)
        return "break"

    def on_close(self):
        if self._maybe_save_changes():
            self.master.destroy()

    # ----- construction -------------------------------------------------
    def __init__(self, master):
        self.master = master
        self.current_file = None

        self.text_area = Text(master, undo=True)
        self.text_area.pack(fill=BOTH, expand=1)
        self.text_area.bind("<<Modified>>", self._on_modified)

        self.main_menu = Menu(master)
        self.master.config(menu=self.main_menu)

        # File menu
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)

        # Edit menu (now correctly bound to its own menu)
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(
            label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        self.edit_menu.add_command(
            label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(
            label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(
            label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)

        # Handle the window close button the same as Exit.
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start from a clean state so a fresh window is not flagged modified.
        self._mark_clean()


if __name__ == "__main__":
    bob = Tk()
    te = text_editor(bob)
    bob.mainloop()
