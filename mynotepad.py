from tkinter import *
from tkinter import filedialog, messagebox
import os


class TextEditor:

    def __init__(self, master):
        self.master = master
        master.title("Untitled - MyNotepad")
        master.geometry("800x600")

        self.current_file = None
        self.modified = False

        self.text_area = Text(master, undo=True, wrap=WORD)
        self.text_area.pack(fill=BOTH, expand=1)
        self.text_area.bind("<<Modified>>", self._on_modified)

        # --- Menu bar ---
        self.main_menu = Menu(master)
        master.config(menu=self.main_menu)

        # File menu
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)

        # Edit menu (fixed: was wrongly pointing to self.file_menu)
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self._cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self._copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self._paste, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Select All", command=self._select_all, accelerator="Ctrl+A")

        # Keyboard shortcuts
        master.bind("<Control-n>", lambda e: self.new_file())
        master.bind("<Control-o>", lambda e: self.open_file())
        master.bind("<Control-s>", lambda e: self.save_file())
        master.bind("<Control-S>", lambda e: self.save_as_file())

        # Window close button
        master.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------- title helpers ----------
    def _update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        dirty = "*" if self.modified else ""
        self.master.title(f"{dirty}{name} - MyNotepad")

    def _on_modified(self, _event=None):
        if self.text_area.edit_modified():
            self.modified = True
            self._update_title()

    def _mark_saved(self):
        self.modified = False
        self.text_area.edit_modified(False)
        self._update_title()

    # ---------- prompt before discard ----------
    def _ask_save_if_dirty(self):
        """Return True if caller may proceed, False if user cancelled."""
        if not self.modified:
            return True
        answer = messagebox.askyesnocancel(
            "Unsaved Changes",
            "Current document has unsaved changes. Save before continuing?"
        )
        if answer is True:
            return self.save_file()
        if answer is False:
            return True          # discard
        return False             # cancel

    # ---------- File operations ----------
    def new_file(self):
        if not self._ask_save_if_dirty():
            return
        self.text_area.delete("1.0", END)
        self.current_file = None
        self._mark_saved()

    def open_file(self):
        if not self._ask_save_if_dirty():
            return
        path = filedialog.askopenfilename(
            title="Open file",
            initialdir=os.path.dirname(self.current_file) if self.current_file else os.getcwd(),
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return  # user cancelled
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Open Error", f"Failed to open file:\n{e}")
            return
        self.text_area.delete("1.0", END)
        self.text_area.insert("1.0", content)
        self.current_file = path
        self._mark_saved()

    def save_file(self):
        if self.current_file is None:
            return self.save_as_file()
        return self._write_to(self.current_file)

    def save_as_file(self):
        path = filedialog.asksaveasfilename(
            title="Save As",
            initialdir=os.path.dirname(self.current_file) if self.current_file else os.getcwd(),
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return False  # user cancelled
        self.current_file = path
        return self._write_to(path)

    def _write_to(self, path):
        try:
            content = self.text_area.get("1.0", END)
            # Text.get always appends a trailing \n; strip the last one for clean saves
            if content.endswith("\n"):
                content = content[:-1]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{e}")
            return False
        self._mark_saved()
        return True

    # ---------- Edit helpers ----------
    def _cut(self):
        self.text_area.event_generate("<<Cut>>")

    def _copy(self):
        self.text_area.event_generate("<<Copy>>")

    def _paste(self):
        self.text_area.event_generate("<<Paste>>")

    def _select_all(self):
        self.text_area.tag_add("sel", "1.0", END)

    # ---------- Close ----------
    def on_close(self):
        if not self._ask_save_if_dirty():
            return
        self.master.destroy()


if __name__ == "__main__":
    bob = Tk()
    te = TextEditor(bob)
    bob.mainloop()
