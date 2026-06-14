#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""launcher.py 的最小验证。

运行方式（在本目录下）：
    python3 -m unittest test_launcher -v
或：
    python3 test_launcher.py

覆盖三个关键流程：
  1. 统一入口：注册表完整、文件都真实存在、覆盖目录里所有示例脚本；
  2. 分组展示：菜单按类型分组、带用途说明；
  3. 启动脚本：真实跑通一个无依赖脚本，前提不满足时友好跳过、运行出错时
     不抛异常，菜单的退出 / 无效选择 / EOF 流程正常。
"""

import io
import os
import unittest
from contextlib import redirect_stdout

import launcher
from launcher import Demo


def _silent_run(demo, **kw):
    """运行 run_script 但吞掉它的打印，返回结果 dict。"""
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = launcher.run_script(demo, **kw)
    return result, buf.getvalue()


class _FakeCompleted:
    """模拟 subprocess.run 的返回对象。"""

    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class UnifiedEntryTests(unittest.TestCase):
    """流程 1：统一入口。"""

    def test_every_registered_file_exists(self):
        for demo in launcher.SCRIPTS:
            path = os.path.join(launcher.BASE_DIR, demo.file)
            self.assertTrue(os.path.isfile(path),
                            "注册的脚本不存在：%s" % demo.file)

    def test_registry_covers_all_example_scripts(self):
        on_disk = {
            f for f in os.listdir(launcher.BASE_DIR)
            if f.endswith(".py")
            and f not in ("launcher.py", os.path.basename(__file__))
        }
        registered = {d.file for d in launcher.SCRIPTS}
        self.assertEqual(on_disk, registered,
                         "目录中的示例脚本与注册表不一致")

    def test_no_duplicate_registrations(self):
        files = [d.file for d in launcher.SCRIPTS]
        self.assertEqual(len(files), len(set(files)), "注册表存在重复脚本")

    def test_ordered_scripts_matches_registry(self):
        self.assertEqual(len(launcher.ordered_scripts()), len(launcher.SCRIPTS))


class GroupedDisplayTests(unittest.TestCase):
    """流程 2：分组展示。"""

    def test_multiple_groups(self):
        groups = launcher.grouped_scripts()
        self.assertGreaterEqual(len(groups), 2, "至少应有多个分组")

    def test_categories_are_known(self):
        for demo in launcher.SCRIPTS:
            self.assertIn(demo.category, launcher.CATEGORY_ORDER,
                          "未知分组：%s" % demo.category)

    def test_menu_shows_groups_and_descriptions(self):
        menu = launcher.render_menu()
        for category, _ in launcher.grouped_scripts():
            self.assertIn(category, menu, "菜单缺少分组：%s" % category)
        # 用途说明（而不仅是文件名）出现在菜单里。
        self.assertIn("登录表单", menu)
        self.assertIn("质数", menu)

    def test_menu_lists_every_script_with_number(self):
        menu = launcher.render_menu()
        for demo in launcher.SCRIPTS:
            self.assertIn(demo.file, menu, "菜单缺少脚本：%s" % demo.file)
        self.assertIn("1)", menu)


class ChoiceParsingTests(unittest.TestCase):
    """流程 3a：编号 / 退出 / 无效选择解析。"""

    def test_quit_aliases(self):
        for raw in ("q", "Q", "quit", "exit", "  q  "):
            self.assertEqual(launcher.parse_choice(raw)[0], "quit")

    def test_list_and_empty(self):
        self.assertEqual(launcher.parse_choice("l")[0], "list")
        self.assertEqual(launcher.parse_choice("")[0], "empty")

    def test_valid_number_returns_demo(self):
        action, payload = launcher.parse_choice("1")
        self.assertEqual(action, "run")
        self.assertEqual(payload, launcher.ordered_scripts()[0])

    def test_out_of_range_and_garbage_are_invalid(self):
        big = str(len(launcher.SCRIPTS) + 999)
        self.assertEqual(launcher.parse_choice(big)[0], "invalid")
        self.assertEqual(launcher.parse_choice("abc")[0], "invalid")
        self.assertEqual(launcher.parse_choice("0")[0], "invalid")


class PreconditionTests(unittest.TestCase):
    """流程 3b：运行前提检查。"""

    def test_console_script_with_no_requirements_passes(self):
        prime = next(d for d in launcher.SCRIPTS if d.file == "prime.py")
        self.assertEqual(launcher.check_preconditions(prime), [])

    def test_missing_module_is_reported(self):
        fake = Demo("prime.py", "stub", "基础语法练习",
                    ["a_module_that_does_not_exist_zzz"], False, [], "")
        problems = launcher.check_preconditions(fake)
        self.assertTrue(any("依赖模块" in p for p in problems))

    def test_missing_data_file_is_reported(self):
        fake = Demo("prime.py", "stub", "基础语法练习",
                    [], False, ["no_such_file.dat"], "")
        problems = launcher.check_preconditions(fake)
        self.assertTrue(any("数据文件" in p for p in problems))

    def test_gui_without_display_is_reported(self):
        saved = {k: os.environ.pop(k, None)
                 for k in ("DISPLAY", "WAYLAND_DISPLAY")}
        try:
            if os.name == "nt" or launcher.sys.platform == "darwin":
                self.skipTest("非 Linux 平台默认认为有显示")
            gui = next(d for d in launcher.SCRIPTS if d.gui)
            problems = launcher.check_preconditions(gui)
            self.assertTrue(any("图形界面" in p for p in problems))
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v


class RunScriptTests(unittest.TestCase):
    """流程 3c：真正启动脚本 / 友好失败。"""

    def test_run_real_console_script(self):
        prime = next(d for d in launcher.SCRIPTS if d.file == "prime.py")
        result, out = _silent_run(prime)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["returncode"], 0)
        self.assertIn("prime no", out)  # prime.py 的真实输出

    def test_missing_requirement_is_skipped_not_raised(self):
        fake = Demo("prime.py", "stub", "基础语法练习",
                    ["a_module_that_does_not_exist_zzz"], False, [], "")
        result, out = _silent_run(fake)
        self.assertEqual(result["status"], "skipped")
        self.assertIn("跳过", out)

    def test_nonzero_exit_is_reported_gracefully(self):
        prime = next(d for d in launcher.SCRIPTS if d.file == "prime.py")
        fake_runner = lambda *a, **k: _FakeCompleted(
            1, stdout="", stderr="Traceback (most recent call last):\nBoom")
        result, out = _silent_run(prime, runner=fake_runner)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["returncode"], 1)
        self.assertIn("运行失败", out)  # 友好提示而非裸异常


class MainLoopTests(unittest.TestCase):
    """流程 3d：交互主循环控制流。"""

    def test_invalid_then_quit(self):
        answers = iter(["zzz", "q"])
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = launcher.main(input_fn=lambda _="": next(answers))
        self.assertEqual(rc, 0)
        self.assertIn("无效选择", buf.getvalue())

    def test_eof_exits_cleanly(self):
        def raise_eof(_=""):
            raise EOFError

        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = launcher.main(input_fn=raise_eof)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
