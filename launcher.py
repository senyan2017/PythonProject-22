#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一入口 / Demo Launcher.

把本仓库里散落的 Tkinter / turtle / 控制台示例脚本集中到一个菜单里，
按类型分组并带上用途说明，挑编号就能运行；运行前会先检查脚本依赖
(图形界面 / 第三方模块 / 数据文件) 是否满足，缺失时给出友好提示，
而不是直接把异常抛到用户脸上。

每个示例脚本仍是独立可单独运行的文件，本入口只是用子进程去调用它们，
并不会修改或替换原有脚本的使用方式。
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from collections import namedtuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 一条示例的元数据。
#   file     : 脚本文件名(相对本目录)
#   title    : 用途说明(给人看的，不只是文件名)
#   category : 所属分组
#   modules  : 运行所需的第三方/可选模块(标准库里一定有的不写)
#   gui      : 是否会弹出图形窗口(需要可用的显示环境)
#   files    : 运行所需的数据文件(相对本目录)
#   note     : 额外提示(可为空)
Demo = namedtuple("Demo", "file title category modules gui files note")

# 分组展示顺序。
CATEGORY_ORDER = [
    "基础表单与控件",
    "文本与文件处理",
    "图形与绘制",
    "基础语法练习",
    "数据库示例",
    "打包脚本",
]

SCRIPTS = [
    # --- 基础表单与控件 ---
    Demo("gui.py", "登录表单：标签+输入框+按钮（pack 布局入门）",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("gridgui.py", "登录表单：grid 网格布局，含按钮点击回调",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("guiplace.py", "place 绝对坐标布局摆放控件演示",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("oopgui.py", "用类(OOP)方式组织 GUI 表单",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("formradio.py", "单选按钮 Radiobutton（性别选择）",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("fromcheck.py", "复选框 Checkbutton 取值演示",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("formlist.py", "列表框 Listbox：显示 / 删除选中项",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("combo.py", "下拉组合框 ttk.Combobox（选择城市）",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("spinbox.py", "数字微调框 Spinbox（1~12）",
         "基础表单与控件", ["tkinter", "cx_Freeze"], True, [],
         "脚本顶部 import cx_Freeze，缺该库会直接报错"),
    Demo("labelframe.py", "标签框架 LabelFrame + Spinbox + Scale 滑块",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("textboxvalue2.py", "单行输入框 Entry + StringVar 取值",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("Graphical.py", "鼠标左 / 中 / 右键点击事件绑定",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("newwindow.py", "弹出子窗口 Toplevel",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("msgbox.py", "弹出消息提示框 messagebox",
         "基础表单与控件", ["tkinter"], True, [], ""),
    Demo("pop.py", "弹出输入对话框 simpledialog",
         "基础表单与控件", ["tkinter"], True, [], ""),

    # --- 文本与文件处理 ---
    Demo("mynotepad.py", "简易记事本：File/Edit 菜单 + 文本区",
         "文本与文件处理", ["tkinter"], True, [],
         "打开对话框默认目录为 Windows 路径 c://"),
    Demo("fontexp.py", "文本编辑器：字体 / 搜索 / 清空 / 显示选中",
         "文本与文件处理", ["tkinter"], True, [], ""),
    Demo("filedialog.py", "文件打开对话框并读取文本内容",
         "文本与文件处理", ["tkinter"], True, [],
         "打开对话框默认目录为 Windows 路径 c://"),
    Demo("scorll.py", "带滚动条 Scrollbar 的列表框",
         "文本与文件处理", ["tkinter"], True, [], ""),
    Demo("filehandlingexp.py", "文件读写与复制（文本 + 图片）",
         "文本与文件处理", [], False,
         ["tech.txt", "techsrijan.txt", "2.jpg"],
         "会在本目录生成 srijan / new.jpg"),

    # --- 图形与绘制 ---
    Demo("canvasexp.py", "Canvas 画布：线 / 矩形 / 椭圆 / 弧 / 多边形",
         "图形与绘制", ["tkinter"], True, [], ""),
    Demo("colorpattern.py", "turtle 随机彩色螺旋",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("colorboxpattern.py", "turtle 渐变彩色螺旋图案",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("coolpattern.py", "turtle 六边形旋转几何图案",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("flag.py", "turtle 绘制印度国旗",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("flag1.py", "turtle 绘制印度国旗（与 flag.py 内容相同）",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("Heart.py", "turtle 绘制爱心",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),
    Demo("sunflower.py", "turtle 绘制向日葵",
         "图形与绘制", ["turtle", "tkinter"], True, [], ""),

    # --- 基础语法练习(纯控制台) ---
    Demo("first.py", "字符串方法演示（capitalize / count / find ...）",
         "基础语法练习", [], False, [], "运行中含 time.sleep 暂停"),
    Demo("prime.py", "打印 10~20 之间的质数",
         "基础语法练习", [], False, [], ""),
    Demo("setexp.py", "集合 set 运算演示（并 / 交 / 差）",
         "基础语法练习", [], False, [], "运行中含 time.sleep 暂停"),
    Demo("EmojiUniCode.py", "打印 Emoji 的 Unicode 字符",
         "基础语法练习", [], False, [], ""),
    Demo("PythonTutorial.py", "打印字符串 / 转义 / Unicode 示例",
         "基础语法练习", [], False, [], ""),

    # --- 数据库示例(需要本机 MySQL) ---
    Demo("dbconfig.py", "pymysql 连接 MySQL（建表 / 增删改查示例）",
         "数据库示例", ["pymysql"], False, [],
         "需本机运行 MySQL（数据库 pythongui）"),
    Demo("dbconnect.py", "pymysql 连接并插入数据",
         "数据库示例", ["pymysql"], False, [],
         "需本机运行 MySQL（数据库 bit）"),
    Demo("textboxvalue.py", "GUI 输入框 + pymysql 写入数据库",
         "数据库示例", ["tkinter", "pymysql"], True, [],
         "需本机运行 MySQL（数据库 pythongui）"),

    # --- 打包脚本(cx_Freeze，非交互演示) ---
    Demo("final.py", "cx_Freeze 打包 gui.py 为可执行文件",
         "打包脚本", ["cx_Freeze"], False, [],
         "Windows 打包脚本，含硬编码路径，非交互演示用"),
    Demo("install.py", "cx_Freeze 安装器脚本",
         "打包脚本", ["cx_Freeze"], False, [],
         "Windows 打包脚本，含硬编码路径，非交互演示用"),
]


def grouped_scripts():
    """按 CATEGORY_ORDER 返回 [(分组名, [Demo, ...]), ...]。"""
    groups = []
    for category in CATEGORY_ORDER:
        items = [d for d in SCRIPTS if d.category == category]
        if items:
            groups.append((category, items))
    return groups


def ordered_scripts():
    """按分组顺序展开成扁平列表，列表下标 + 1 即为菜单编号。"""
    flat = []
    for _, items in grouped_scripts():
        flat.extend(items)
    return flat


def _gui_available():
    """粗略判断当前环境是否有可用的图形显示。"""
    if sys.platform.startswith("win") or sys.platform == "darwin":
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def check_preconditions(demo):
    """检查脚本运行前提，返回缺失项说明列表（空列表表示满足）。"""
    problems = []
    for module in demo.modules:
        if importlib.util.find_spec(module) is None:
            problems.append("缺少依赖模块：%s" % module)
    if demo.gui and not _gui_available():
        problems.append("需要图形界面(GUI)环境，但当前没有可用显示")
    for name in demo.files:
        if not os.path.exists(os.path.join(BASE_DIR, name)):
            problems.append("缺少数据文件：%s" % name)
    return problems


def render_menu(scripts=None):
    """生成分组后的菜单文本。"""
    if scripts is None:
        scripts = ordered_scripts()
    width = max((len(d.file) for d in scripts), default=0)
    lines = [
        "=" * 60,
        "  Tkinter / Python 示例统一入口 (Demo Launcher)",
        "=" * 60,
    ]
    index = 0
    for category, items in grouped_scripts():
        lines.append("")
        lines.append("[%s]" % category)
        for demo in items:
            index += 1
            lines.append(
                "  %2d) %-*s  - %s" % (index, width, demo.file, demo.title)
            )
            if demo.note:
                lines.append("      %s* %s" % (" " * width, demo.note))
    lines.append("")
    lines.append("操作：输入编号运行示例 | l 重新列出 | q 退出")
    return "\n".join(lines)


def run_script(demo, runner=subprocess.run):
    """运行单个示例脚本。

    返回 dict: {status, reason, returncode}
        status: "ok" 正常结束 / "skipped" 前提不满足 / "failed" 运行出错
    先做前提检查，缺什么就友好提示并跳过，不抛异常。
    """
    problems = check_preconditions(demo)
    if problems:
        print("\n[跳过] %s —— 运行前提不满足：" % demo.file)
        for p in problems:
            print("   - " + p)
        return {"status": "skipped", "reason": "; ".join(problems),
                "returncode": None}

    path = os.path.join(BASE_DIR, demo.file)
    print("\n[运行] %s —— %s" % (demo.file, demo.title))
    if demo.gui:
        print("   (会弹出窗口，关闭窗口后返回菜单)")
    try:
        result = runner(
            [sys.executable, path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )
    except OSError as exc:  # 启动子进程本身就失败
        print("   启动失败：%s" % exc)
        return {"status": "failed", "reason": str(exc), "returncode": None}

    if result.stdout:
        print("   --- 输出 ---")
        print(result.stdout.rstrip("\n"))

    if result.returncode == 0:
        print("   完成（退出码 0）")
        return {"status": "ok", "reason": "", "returncode": 0}

    # 非零退出：给出友好提示 + 末尾几行错误信息，而不是整段堆栈直接糊脸。
    print("   运行失败（退出码 %s）。" % result.returncode)
    err = (result.stderr or "").rstrip("\n")
    if err:
        tail = err.splitlines()[-15:]
        print("   错误信息（末尾片段）：")
        for line in tail:
            print("     " + line)
    return {"status": "failed", "reason": err, "returncode": result.returncode}


def parse_choice(raw, scripts=None):
    """解析用户输入，返回 (action, payload)。

    action: "quit" / "list" / "empty" / "invalid" / "run"
    payload: action=="run" 时为对应的 Demo，否则为原始输入。
    纯函数，方便测试无效选择 / 退出 / 编号解析。
    """
    if scripts is None:
        scripts = ordered_scripts()
    text = (raw or "").strip().lower()
    if text in ("q", "quit", "exit"):
        return ("quit", text)
    if text in ("l", "list"):
        return ("list", text)
    if text == "":
        return ("empty", text)
    if text.isdigit():
        num = int(text)
        if 1 <= num <= len(scripts):
            return ("run", scripts[num - 1])
        return ("invalid", raw)
    return ("invalid", raw)


def main(input_fn=input, scripts=None):
    """交互主循环。input_fn 可注入以便测试。"""
    if scripts is None:
        scripts = ordered_scripts()
    print(render_menu(scripts))
    while True:
        try:
            raw = input_fn("\n> ")
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            return 0

        action, payload = parse_choice(raw, scripts)
        if action == "quit":
            print("再见！")
            return 0
        if action == "list":
            print(render_menu(scripts))
        elif action == "empty":
            continue
        elif action == "invalid":
            print("无效选择：%r —— 请输入菜单中的编号，或 l 列出 / q 退出。"
                  % (payload,))
        elif action == "run":
            run_script(payload)


if __name__ == "__main__":
    sys.exit(main())
