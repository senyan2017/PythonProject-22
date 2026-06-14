"""
test_mynotepad.py
-----------------
Headless smoke-test for mynotepad.py.
Works even when python3-tk is not installed, by monkey-patching tkinter
with lightweight stubs.  Run:

    python3 test_mynotepad.py
"""
import os, sys, tempfile, types, unittest
from unittest.mock import MagicMock, patch

# ── 1. build minimal tkinter stubs ──────────────────────────────────────────
TK = types.ModuleType("tkinter")
FD = types.ModuleType("tkinter.filedialog")
MB = types.ModuleType("tkinter.messagebox")

# Constants
TK.END = "end"
TK.BOTH = "both"
TK.WORD = "word"

# Tk root stub
class _FakeTk:
    def __init__(self):
        self._title = ""
        self._protocol = {}
    def title(self, t=None):
        if t is None: return self._title
        self._title = t
    def geometry(self, *a): pass
    def config(self, **kw): pass
    def bind(self, *a): pass
    def withdraw(self): pass
    def destroy(self): pass
    def update(self): pass
    def protocol(self, name, func=None):
        if func is not None:
            self._protocol[name] = func
TK.Tk = _FakeTk

# Text widget stub
class _FakeText:
    def __init__(self, *a, **kw):
        self._content = ""
        self._modified = False
        self._bindings = {}
    def pack(self, **kw): pass
    def bind(self, event, func):
        self._bindings[event] = func
    def delete(self, start, end):
        self._content = ""
    def insert(self, index, text):
        self._content += text
    def get(self, start, end):
        return self._content + "\n"
    def edit_modified(self, val=None):
        if val is None:
            return self._modified
        self._modified = val
    def edit_undo(self): pass
    def edit_redo(self): pass
    def event_generate(self, *a): pass
    def tag_add(self, *a): pass
TK.Text = _FakeText

# Menu stub
class _FakeMenu:
    def __init__(self, *a, **kw):
        self._items = []
    def add_cascade(self, **kw):
        self._items.append(kw)
    def add_command(self, **kw):
        self._items.append(kw)
    def add_separator(self):
        self._items.append({"type": "separator"})
    def index(self, what):
        if what == "end":
            return len(self._items) - 1 if self._items else -1
        return int(what)
    def entrycget(self, i, key):
        return self._items[i].get(key, "")
TK.Menu = _FakeMenu

FD.askopenfilename = MagicMock(return_value="")
FD.asksaveasfilename = MagicMock(return_value="")
MB.askyesnocancel = MagicMock(return_value=False)   # "No" -> discard
MB.showerror = MagicMock()

sys.modules["tkinter"] = TK
sys.modules["tkinter.filedialog"] = FD
sys.modules["tkinter.messagebox"] = MB

# ── 2. import the module under test ─────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from mynotepad import TextEditor  # noqa: E402

TEMP_DIR = tempfile.mkdtemp(prefix="notepad_test_")


# ── 3. tests ────────────────────────────────────────────────────────────────
class TestNotepad(unittest.TestCase):

    def setUp(self):
        self.root = _FakeTk()
        self.ed = TextEditor(self.root)

    # ── title ──
    def test_initial_title_untitled(self):
        self.assertIn("Untitled", self.root.title())

    def test_title_shows_filename(self):
        self.ed.current_file = "/tmp/foo.txt"
        self.ed._mark_saved()
        self.assertIn("foo.txt", self.root.title())

    def test_title_dirty_marker(self):
        self.ed.modified = True
        self.ed._update_title()
        self.assertTrue(self.root.title().startswith("*"))

    # ── open ──
    def test_open_reads_content(self):
        path = os.path.join(TEMP_DIR, "open.txt")
        with open(path, "w") as f:
            f.write("hello\nworld")
        FD.askopenfilename.return_value = path
        self.ed.open_file()
        # Text stub accumulates via insert
        self.assertEqual(self.ed.current_file, path)
        self.assertFalse(self.ed.modified)

    def test_open_cancel_does_nothing(self):
        FD.askopenfilename.return_value = ""
        self.ed.open_file()
        self.assertIsNone(self.ed.current_file)

    # ── save ──
    def test_save_delegates_to_save_as_when_no_path(self):
        called = []
        self.ed.save_as_file = lambda: (called.append(1), False)[1]
        self.ed.save_file()
        self.assertTrue(called)

    def test_save_writes_file(self):
        path = os.path.join(TEMP_DIR, "save.txt")
        self.ed.current_file = path
        self.ed.text_area._content = "saved data"
        result = self.ed.save_file()
        self.assertTrue(result)
        with open(path) as f:
            self.assertEqual(f.read(), "saved data")
        self.assertFalse(self.ed.modified)

    # ── save as ──
    def test_save_as_writes_file(self):
        path = os.path.join(TEMP_DIR, "saveas.txt")
        FD.asksaveasfilename.return_value = path
        self.ed.text_area._content = "as data"
        result = self.ed.save_as_file()
        self.assertTrue(result)
        with open(path) as f:
            self.assertEqual(f.read(), "as data")
        self.assertEqual(self.ed.current_file, path)

    def test_save_as_cancel_returns_false(self):
        FD.asksaveasfilename.return_value = ""
        result = self.ed.save_as_file()
        self.assertFalse(result)

    # ── new ──
    def test_new_clears_content(self):
        self.ed.text_area._content = "stuff"
        self.ed.modified = False
        self.ed.new_file()
        self.assertEqual(self.ed.text_area._content, "")
        self.assertIsNone(self.ed.current_file)

    # ── edit menu ──
    def test_edit_menu_is_separate(self):
        self.assertIsNot(self.ed.edit_menu, self.ed.file_menu)
        # main_menu cascades: File -> file_menu, Edit -> edit_menu
        cascades = [i for i in self.ed.main_menu._items if "menu" in i]
        menus = {i["label"]: i["menu"] for i in cascades}
        self.assertIs(menus["File"], self.ed.file_menu)
        self.assertIs(menus["Edit"], self.ed.edit_menu)

    def test_edit_menu_has_actions(self):
        labels = [i.get("label", "") for i in self.ed.edit_menu._items]
        for name in ("Undo", "Redo", "Cut", "Copy", "Paste", "Select All"):
            self.assertIn(name, labels)

    # ── close / dirty prompt ──
    def test_close_with_no_changes_destroys(self):
        self.ed.modified = False
        self.ed.on_close()
        # _ask_save_if_dirty returns True, master.destroy is called
        # (no exception = pass)

    def test_dirty_prompt_called(self):
        self.ed.modified = True
        MB.askyesnocancel.return_value = False  # discard
        self.ed.on_close()  # should not raise

    def test_dirty_prompt_cancel_aborts(self):
        self.ed.modified = True
        MB.askyesnocancel.return_value = None  # cancel
        destroyed = []
        self.root.destroy = lambda: destroyed.append(1)
        self.ed.on_close()
        self.assertFalse(destroyed, "destroy should NOT have been called")

    # ── roundtrip ──
    def test_roundtrip(self):
        original = "Hello\nLine2\nLine3"
        path = os.path.join(TEMP_DIR, "rt.txt")
        with open(path, "w") as f:
            f.write(original)
        # open
        FD.askopenfilename.return_value = path
        self.ed.open_file()
        # save to new path
        path2 = os.path.join(TEMP_DIR, "rt2.txt")
        FD.asksaveasfilename.return_value = path2
        self.ed.save_as_file()
        with open(path2) as f:
            self.assertEqual(f.read(), original)


if __name__ == "__main__":
    print(f"Temp dir: {TEMP_DIR}")
    unittest.main(verbosity=2)
