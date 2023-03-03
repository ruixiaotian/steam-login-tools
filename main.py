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
import os
# import cgitb
from ui import SteamLoginUI, QApplication


def main():
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
    log_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    cgitb.enable(display=0, format='log', logdir=log_dir, context=10)


if __name__ == '__main__':
    main()
