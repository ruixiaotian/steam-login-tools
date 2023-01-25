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
from ui import SteamLoginUI, QApplication


def main():
    app = QApplication(sys.argv)
    win = SteamLoginUI()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
