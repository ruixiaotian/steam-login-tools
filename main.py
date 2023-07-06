#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 0:38
# @Author  : 桥话语权
# @File    : main.py
# @Software: PyCharm
"""
程序的主入口~
"""
import cgitb
import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from creart import create
from loguru import logger

from Ui import SteamLoginUI

LOGO = r"""

███████╗████████╗███████╗ █████╗ ███╗   ███╗      ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║      ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
███████╗   ██║   █████╗  ███████║██╔████╔██║█████╗██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
╚════██║   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║╚════╝██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║      ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
"""


def main():
    rush_backtracking()
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
    app = QApplication(sys.argv)
    create(SteamLoginUI).show()
    sys.exit(app.exec())


def rush_backtracking():
    """奔溃回溯,如果程序引发了崩溃,将会在桌面生成崩溃日志"""
    log_dir = Path.home() / "Desktop"
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    cgitb.enable(display=0, format="log", logdir=str(log_dir), context=10)


if __name__ == "__main__":
    # 打印一个华丽的LOGO
    logger.opt(colors=True).info(f"<blue>{LOGO}</>")
    main()
