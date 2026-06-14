#!/usr/bin/env python3
"""
统一入口验证脚本 (verify_launcher.py)
=====================================
以非交互方式快速验证 launcher.py 的三个关键流程：
  1. 分组展示 —— 注册表结构是否完整
  2. 脚本启动 —— run_script 对合法/非法文件的处理
  3. CLI --list —— 终端输出是否正常

运行方式：
    python verify_launcher.py

无需显示器，无需 tkinter 窗口。全部通过即打印 "ALL PASSED"。
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
passed = 0
failed = 0


def check(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}  —  {detail}")
        failed += 1


# ===================================================================
# 1. 模块导入 & 注册表结构
# ===================================================================
print("\n=== 1. 注册表结构验证 ===")

sys.path.insert(0, BASE_DIR)
try:
    import launcher
    check("launcher.py 可正常导入", True)
except Exception as e:
    check("launcher.py 可正常导入", False, str(e))
    print("\n无法继续验证，launcher.py 导入失败。")
    sys.exit(1)

scripts_dict = launcher.SCRIPTS
check("SCRIPTS 是非空 dict", isinstance(scripts_dict, dict) and len(scripts_dict) > 0,
      f"type={type(scripts_dict)}, len={len(scripts_dict)}")

# 检查至少有几个分组
check("分组数 >= 5", len(scripts_dict) >= 5,
      f"实际分组数: {len(scripts_dict)}")

# 每个分组都是 list，每个条目是 (filename, desc, dep) 三元组
all_ok = True
total_scripts = 0
for cat, items in scripts_dict.items():
    if not isinstance(items, list):
        all_ok = False
        break
    for item in items:
        total_scripts += 1
        if not isinstance(item, tuple) or len(item) != 3:
            all_ok = False
            break

check("所有条目均为 (filename, desc, dep) 三元组", all_ok)
check(f"总脚本数 > 0 (实际: {total_scripts})", total_scripts > 0)

# 验证关键脚本都在注册表中
all_files = [item[0] for items in scripts_dict.values() for item in items]
for key_script in ["gui.py", "mynotepad.py", "formradio.py", "formlist.py", "gridgui.py"]:
    check(f"关键脚本 {key_script} 已注册", key_script in all_files,
          f"未在 SCRIPTS 中找到 {key_script}")

# 验证注册的文件确实存在
missing = [f for f in all_files if not os.path.isfile(os.path.join(BASE_DIR, f))]
check("所有注册文件均存在于磁盘", len(missing) == 0,
      f"缺失文件: {missing}" if missing else "")


# ===================================================================
# 2. run_script 函数验证
# ===================================================================
print("\n=== 2. 脚本启动函数验证 ===")

# 2a. 对不存在的文件应返回失败
success, msg = launcher.run_script("this_does_not_exist.py")
check("不存在的文件返回失败", not success, f"success={success}, msg={msg}")

# 2b. 对一个纯打印脚本应成功启动（用 PythonTutorial.py 因为它只是 print）
success, msg = launcher.run_script("PythonTutorial.py")
check("PythonTutorial.py 启动成功", success, f"msg={msg}")

# 2c. 对一个简单计算脚本应成功启动
success, msg = launcher.run_script("prime.py")
check("prime.py 启动成功", success, f"msg={msg}")

# 2d. EmojiUniCode.py 只是 print，应该成功
success, msg = launcher.run_script("EmojiUniCode.py")
check("EmojiUniCode.py 启动成功", success, f"msg={msg}")


# ===================================================================
# 3. CLI --list 模式验证
# ===================================================================
print("\n=== 3. CLI --list 输出验证 ===")

result = subprocess.run(
    [sys.executable, os.path.join(BASE_DIR, "launcher.py"), "--list"],
    capture_output=True, text=True, timeout=10
)
check("--list 退出码为 0", result.returncode == 0,
      f"returncode={result.returncode}, stderr={result.stderr[:200]}")

output = result.stdout
check("--list 输出包含 '基础表单'", "基础表单" in output)
check("--list 输出包含 'Turtle'", "Turtle" in output)
check("--list 输出包含 'gui.py'", "gui.py" in output)
check("--list 输出包含 'mynotepad.py'", "mynotepad.py" in output)
check("--list 输出包含分组数统计", "个分组" in output)


# ===================================================================
# 汇总
# ===================================================================
print(f"\n{'=' * 50}")
print(f"  通过: {passed}    失败: {failed}    总计: {passed + failed}")
print(f"{'=' * 50}")

if failed == 0:
    print("\n  ✓ ALL PASSED — 统一入口验证全部通过\n")
    sys.exit(0)
else:
    print(f"\n  ✗ {failed} 项失败，请检查上方详情\n")
    sys.exit(1)
