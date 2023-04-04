#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 0:38
# @Author  : 桥话语权
# @File    : main.py
# @Software: PyCharm
"""
程序的主入口~
"""
import sys
from pathlib import Path
# import cgitb
from loguru import logger
from ui import SteamLoginUI, QApplication


LOGO = r"""

███████╗████████╗███████╗ █████╗ ███╗   ███╗      ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║      ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
███████╗   ██║   █████╗  ███████║██╔████╔██║█████╗██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
╚════██║   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║╚════╝██║     ██║   ██║██║   ██║██║██║╚██╗██║
███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║      ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝

"""

def main():
    # 打印一个华丽LOGO
    logger.opt(colors=True).info(f"<blue>{LOGO}</>")
    # rush_backtracking()
    app = QApplication(sys.argv)
    win = SteamLoginUI()
    win.show()
    sys.exit(app.exec())


def rush_backtracking():
    """
    奔溃回溯,如果程序引发了崩溃,将会在桌面生成崩溃日志
    :return:
    """
    log_dir = Path.home() / 'Desktop'
    if not log_dir.exists():
        log_dir.mkdir()
    cgitb.enable(display=0, format='log', logdir=str(log_dir), context=10)


if __name__ == '__main__':
    main()
