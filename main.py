#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :main.py
# @Time :2023-7-20 上午 10:10
# @Author :Qiao
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from creart import create

from Ui import MainWindow
from Core.FileFunction import JsonFunc

if __name__ == "__main__":

    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # 检查文件
    create(JsonFunc).checkDataFile()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
