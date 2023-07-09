#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :DownloadThread.py
# @Time :2023-7-7 下午 07:39
# @Author :Qiao
import sys
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
from creart import add_creator, create, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui import SteamLoginUI
from Ui.Share import shadow_setup


class DownloadQDialog(QMainWindow):
    close_state = True

    def __init__(self):
        super().__init__()
        self.setup_form()

    def initialize(self, parent: QMainWindow):
        """初始化"""
        # self.setParent(parent)  # 设置父窗体
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体
        self.setWindowModality(Qt.WindowModal)  # 设置模态
        self.setObjectName("DownloadQDialog")  # 设置对象名称
        self.setStyleSheet(create(SteamLoginUI).qss_content)  # 设置qss
        self.font = create(SteamLoginUI).font_name  # 设置字体名称

    def setup_form(self) -> None:
        """窗体设定"""
        # 透明窗体
        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setObjectName("base_widget")  # 设置对象名称
        self.base_layout = QGridLayout()  # 创建透明窗口布局
        self.base_widget.setLayout(self.base_layout)  # 设置布局
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏背景

        # 主窗体
        self.main_widget = QWidget()  # 创建主窗体
        self.main_widget.setObjectName("main_widget")  # 设置主窗体对象名称
        self.base_layout.addWidget(self.main_widget)  # 添加到布局

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 添加阴影
        shadow_setup(self.main_widget, (0, 1), 12, QColor("#1DBEF5"))

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """重构鼠标按下事件函数,进行鼠标跟踪以及获取相对位置"""
        if event.button() == Qt.LeftButton:
            # 如果按下按钮为左键
            self._mouse_flag = True  # 设置鼠标跟踪开关为True
            self.m_pos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """重构鼠标移动事件函数,进行监控鼠标移动并且判断是否拖动窗口"""
        if Qt.LeftButton and self._mouse_flag and self.close_state:
            # 如果是左键按下鼠标且跟踪打开, 不处于关闭状态,则可以拖动窗口
            self.move(event.globalPos() - self.m_pos)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """重构鼠标松开事件函数,进行监控鼠标状态"""
        self._mouse_flag = False  # 设置鼠标跟踪为关


class DownloadQDialogClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo("Core.NetworkThreads.DownloadThread", "DownloadQDialog"),
    )

    # 静态方法available()，用于检查模块"DownloadQDialog"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Core.NetworkThreads.DownloadThread")

    # 静态方法create()，用于创建DownloadQDialog类的实例，返回值为DownloadQDialog对象。
    @staticmethod
    def create(create_type: [DownloadQDialog]) -> DownloadQDialog:
        return DownloadQDialog()


add_creator(DownloadQDialogClassCreator)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DownloadQDialog()
    win.show()
    sys.exit(app.exec())
