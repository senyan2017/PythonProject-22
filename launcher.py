#!/usr/bin/env python3
"""
Tkinter 示例统一入口 (Launcher)
================================
将所有 Tkinter / Turtle / Python 基础示例按类别整理到一个可选择的列表中，
点击即可运行对应脚本。原有脚本文件不做任何修改，仍可独立运行。

用法：
    python launcher.py          # GUI 模式（需要显示器/tkinter）
    python launcher.py --list   # 仅打印分组列表（无需 GUI 环境）
"""

import os
import sys
import subprocess
import importlib

# ---------------------------------------------------------------------------
# 脚本注册表 —— 按类别分组，每个条目 (文件名, 中文说明, 额外依赖提示)
# ---------------------------------------------------------------------------
SCRIPTS = {
    "基础表单 (Basic Forms)": [
        ("gui.py",           "基础登录表单 — Label/Entry/Button + pack 布局",      None),
        ("gridgui.py",       "Grid 布局登录表单 — 用户名/密码 + Login 按钮",        None),
        ("guiplace.py",      "Place 绝对定位表单 — 用户名/密码标签",                None),
        ("oopgui.py",        "OOP 风格 GUI 表单 — 面向对象写法示例",                None),
        ("Graphical.py",     "鼠标事件绑定 — 左/中/右键点击回调",                   None),
        ("newwindow.py",     "打开新窗口 — Toplevel 子窗口示例",                    None),
    ],
    "表单控件 (Form Controls)": [
        ("formradio.py",     "单选框 Radiobutton — 性别选择示例",                   None),
        ("fromcheck.py",     "复选框 Checkbutton — 语言勾选示例",                   None),
        ("formlist.py",      "列表框 Listbox — 多选/删除操作",                      None),
        ("combo.py",         "下拉框 Combobox — 城市选择示例",                      None),
        ("spinbox.py",       "数值微调框 Spinbox — 1~12 选择",                      None),
        ("labelframe.py",    "LabelFrame + Spinbox + Scale 滑块组合",               None),
        ("scorll.py",        "滚动条 Scrollbar + Listbox 联动",                     None),
        ("textboxvalue.py",  "文本框取值 — Entry + 写入 MySQL 数据库",              "pymysql"),
        ("textboxvalue2.py", "文本框取值 — StringVar 绑定示例",                     None),
        ("fontexp.py",       "字体实验 — Text 控件 + 系统字体列表",                 None),
    ],
    "对话框 (Dialogs)": [
        ("msgbox.py",        "消息对话框 — messagebox.showinfo 示例",               None),
        ("pop.py",           "输入对话框 — simpledialog.askinteger 示例",            None),
        ("filedialog.py",    "文件选择对话框 — filedialog.askopenfile 示例",         None),
    ],
    "应用程序 (Applications)": [
        ("mynotepad.py",     "简易记事本 — 文本编辑器(打开/保存/退出)",              None),
    ],
    "Turtle 图形 (Turtle Graphics)": [
        ("canvasexp.py",     "Canvas 绘图 — 线条/矩形/椭圆/弧线/多边形",           None),
        ("colorboxpattern.py","Turtle 彩色螺旋图案 — RGB 渐变色",                   None),
        ("colorpattern.py",  "Turtle 随机彩色螺旋 — 随机 RGB 颜色",                None),
        ("coolpattern.py",   "Turtle 酷炫几何图案 — 对称多边形",                   None),
        ("flag.py",          "Turtle 画国旗 — 印度国旗(三色)",                      None),
        ("flag1.py",         "Turtle 画国旗 — 印度国旗变体",                        None),
        ("Heart.py",         "Turtle 画爱心 — 红色填充心形",                        None),
        ("sunflower.py",     "Turtle 画向日葵 — 花瓣+葵花",                         None),
    ],
    "Python 基础 (Python Basics)": [
        ("first.py",         "字符串操作 — capitalize/count/find/split 等",         None),
        ("prime.py",         "素数判断 — 10~20 范围素数检测",                       None),
        ("setexp.py",        "集合操作 — set/frozenset 增删查",                     None),
        ("EmojiUniCode.py",  "Unicode Emoji — 打印表情符号",                        None),
        ("PythonTutorial.py","Python 基础打印 — 字符串/Unicode 演示",               None),
        ("filehandlingexp.py","文件读写操作 — 文本/图片拷贝(依赖 tech.txt 等)",      "文件依赖"),
    ],
    "数据库 (Database)": [
        ("dbconfig.py",      "MySQL 连接配置 — pymysql 建表(需本地 MySQL)",         "pymysql + MySQL"),
        ("dbconnect.py",     "MySQL 数据操作 — 增删改查(需本地 MySQL)",             "pymysql + MySQL"),
    ],
    "打包工具 (Build Tools)": [
        ("final.py",         "cx_Freeze 打包脚本 — 生成可执行文件",                 "cx_Freeze"),
        ("install.py",       "cx_Freeze 安装脚本 — Windows 安装器",                 "cx_Freeze"),
    ],
}

# 项目根目录 = 本脚本所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# CLI 模式：--list
# ---------------------------------------------------------------------------
def print_list():
    """在终端打印所有分组和脚本，无需 GUI 环境。"""
    for category, items in SCRIPTS.items():
        print(f"\n{'=' * 60}")
        print(f"  {category}")
        print(f"{'=' * 60}")
        for filename, desc, dep in items:
            dep_note = f"  [依赖: {dep}]" if dep else ""
            print(f"  - {filename:<24s} {desc}{dep_note}")
    print(f"\n共 {sum(len(v) for v in SCRIPTS.values())} 个脚本，"
          f"{len(SCRIPTS)} 个分组")


# ---------------------------------------------------------------------------
# 脚本启动器
# ---------------------------------------------------------------------------
def run_script(filename):
    """
    以子进程方式运行脚本，返回 (success: bool, message: str)。
    不捕获子进程的 stdout/stderr，让它们在各自窗口中正常输出。
    """
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(filepath):
        return False, f"文件不存在: {filename}"

    try:
        proc = subprocess.Popen(
            [sys.executable, filepath],
            cwd=BASE_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # 等待一小段时间看脚本是否立刻崩溃（<1 秒）
        try:
            proc.wait(timeout=1.5)
            # 如果进程已经退出且返回码非 0，说明启动失败
            if proc.returncode != 0:
                stderr_output = proc.stderr.read().decode("utf-8", errors="replace")
                # 提取最后一行有意义的错误
                err_lines = [l for l in stderr_output.strip().splitlines() if l.strip()]
                err_msg = err_lines[-1] if err_lines else f"退出码 {proc.returncode}"
                return False, f"{filename} 启动失败:\n{err_msg}"
        except subprocess.TimeoutExpired:
            # 脚本仍在运行（正常情况，如 GUI mainloop）
            pass

        return True, f"{filename} 已启动"

    except Exception as e:
        return False, f"启动 {filename} 时出错:\n{e}"


# ---------------------------------------------------------------------------
# GUI 模式 —— 主启动器界面
# ---------------------------------------------------------------------------
def launch_gui():
    """创建并运行 Tkinter 启动器主窗口。"""
    try:
        from tkinter import Tk, Frame, Label, Button, Listbox, Scrollbar
        from tkinter import messagebox, END, SINGLE, EXTENDED
    except ImportError:
        print("[错误] 无法导入 tkinter，请确保已安装 Tk 支持。")
        print("  Linux:  sudo apt install python3-tk")
        print("  macOS:  brew install python-tk")
        sys.exit(1)

    # ---- 主窗口 ----
    root = Tk()
    root.title("Tkinter 示例启动器")
    root.geometry("780x580+100+80")
    root.configure(bg="#f0f0f0")

    # ---- 顶部标题 ----
    header = Frame(root, bg="#2c3e50", height=50)
    header.pack(fill="x")
    header.pack_propagate(False)
    Label(header, text="Tkinter 示例启动器",
          font=("Microsoft YaHei", 16, "bold"),
          fg="white", bg="#2c3e50").pack(expand=True)

    # ---- 主体区域 ----
    body = Frame(root, bg="#f0f0f0")
    body.pack(fill="both", expand=True, padx=10, pady=8)

    # 左侧：分组列表
    left = Frame(body, bg="#f0f0f0")
    left.pack(side="left", fill="both", expand=True)

    Label(left, text="选择分类:", font=("Microsoft YaHei", 11, "bold"),
          bg="#f0f0f0", anchor="w").pack(fill="x", pady=(0, 4))

    cat_scroll = Scrollbar(left)
    cat_scroll.pack(side="right", fill="y")
    cat_listbox = Listbox(left, font=("Microsoft YaHei", 10),
                          selectmode=SINGLE, yscrollcommand=cat_scroll.set,
                          activestyle="dotbox", selectbackground="#3498db",
                          selectforeground="white")
    cat_listbox.pack(fill="both", expand=True)
    cat_scroll.config(command=cat_listbox.yview)

    categories = list(SCRIPTS.keys())
    for cat in categories:
        count = len(SCRIPTS[cat])
        cat_listbox.insert(END, f"  {cat}  ({count} 个示例)")

    # 右侧：脚本列表
    right = Frame(body, bg="#f0f0f0")
    right.pack(side="right", fill="both", expand=True, padx=(10, 0))

    Label(right, text="示例列表:", font=("Microsoft YaHei", 11, "bold"),
          bg="#f0f0f0", anchor="w").pack(fill="x", pady=(0, 4))

    script_scroll = Scrollbar(right)
    script_scroll.pack(side="right", fill="y")
    script_listbox = Listbox(right, font=("Microsoft YaHei", 9),
                             selectmode=SINGLE, yscrollcommand=script_scroll.set,
                             activestyle="dotbox", selectbackground="#27ae60",
                             selectforeground="white")
    script_listbox.pack(fill="both", expand=True)
    script_scroll.config(command=script_listbox.yview)

    # 状态栏
    status_var = Label(root, text="就绪 — 请选择分类和示例",
                       font=("Microsoft YaHei", 9), bg="#ecf0f1",
                       anchor="w", padx=8)
    status_var.pack(fill="x", side="bottom")

    # 当前选中分类的脚本数据 (filename, desc, dep)
    current_scripts = []

    def refresh_script_list(_event=None):
        """左侧分类变化时刷新右侧脚本列表。"""
        nonlocal current_scripts
        sel = cat_listbox.curselection()
        if not sel:
            return
        cat_name = categories[sel[0]]
        current_scripts = SCRIPTS[cat_name]

        script_listbox.delete(0, END)
        for filename, desc, dep in current_scripts:
            dep_tag = f"  [{dep}]" if dep else ""
            script_listbox.insert(END, f"  {filename:<22s} {desc}{dep_tag}")
        status_var.config(text=f"已选择分类: {cat_name}")

    cat_listbox.bind("<<ListboxSelect>>", refresh_script_list)

    def on_run():
        """运行按钮回调：启动选中的脚本。"""
        sel = script_listbox.curselection()
        if not sel:
            messagebox.showwarning("未选择", "请先在右侧列表中选择一个示例脚本。")
            return
        idx = sel[0]
        if idx >= len(current_scripts):
            messagebox.showwarning("无效选择", "选择无效，请重新选择。")
            return
        filename, desc, dep = current_scripts[idx]
        status_var.config(text=f"正在启动: {filename} ...")
        root.update_idletasks()

        success, msg = run_script(filename)
        if success:
            status_var.config(text=f"✓ {msg}")
        else:
            status_var.config(text=f"✗ {filename} 启动失败")
            messagebox.showerror("启动失败", msg)

    def on_show_info():
        """显示选中脚本的详细信息。"""
        sel = script_listbox.curselection()
        if not sel:
            messagebox.showinfo("提示", "请先选择一个示例脚本。")
            return
        idx = sel[0]
        if idx >= len(current_scripts):
            return
        filename, desc, dep = current_scripts[idx]
        info = f"文件: {filename}\n\n说明: {desc}"
        if dep:
            info += f"\n\n额外依赖: {dep}"
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            info += f"\n文件大小: {size} 字节"
        messagebox.showinfo("脚本详情", info)

    def on_exit():
        """退出按钮回调。"""
        if messagebox.askyesno("退出", "确定要退出启动器吗？"):
            root.destroy()

    # ---- 底部按钮栏 ----
    btn_frame = Frame(root, bg="#f0f0f0")
    btn_frame.pack(fill="x", padx=10, pady=(0, 6))

    run_btn = Button(btn_frame, text="▶ 运行选中示例", font=("Microsoft YaHei", 10, "bold"),
                     bg="#27ae60", fg="white", width=18, command=on_run)
    run_btn.pack(side="left", padx=(0, 8))

    info_btn = Button(btn_frame, text="ℹ 查看详情", font=("Microsoft YaHei", 10),
                      bg="#3498db", fg="white", width=14, command=on_show_info)
    info_btn.pack(side="left", padx=(0, 8))

    exit_btn = Button(btn_frame, text="✕ 退出", font=("Microsoft YaHei", 10),
                      bg="#e74c3c", fg="white", width=10, command=on_exit)
    exit_btn.pack(side="right")

    # 双击运行
    script_listbox.bind("<Double-Button-1>", lambda e: on_run())

    # 键盘 Enter 运行
    script_listbox.bind("<Return>", lambda e: on_run())

    # 默认选中第一个分类
    cat_listbox.selection_set(0)
    refresh_script_list()

    # 窗口关闭按钮
    root.protocol("WM_DELETE_WINDOW", on_exit)

    root.mainloop()


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if "--list" in sys.argv:
        print_list()
    else:
        launch_gui()
