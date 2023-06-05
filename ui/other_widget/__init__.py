from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QCheckBox, QAction, \
    QSizePolicy, QCompleter, QGraphicsDropShadowEffect, QScrollArea, QMenu, QSpacerItem, QDialog, QStackedWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPainter, QMouseEvent, QCloseEvent
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
from typing import List
from pathlib import Path

from core.file_operation import FileOperation

from creart import create, exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo
from abc import ABC

from .share import shadow_setup
from .path_card import path_page

import json


class DownloadWidget:

    def __init__(self):
        pass

    def initialize(self, parent: QMainWindow, font: str, page: QStackedWidget):
        self.parent = parent
        self.font = font
        self.page = page

    def dw_widget_setup(self):
        """
        设置界面
        :return:
        """
        # 创建页面
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(390, 500)
        widget.setObjectName('dw_widget')

        # 添加到布局
        layout.addWidget(self.dw_title(), 1, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.loop_widget(), 2, 0, 1, 1, Qt.AlignTop)

        layout.setContentsMargins(0, 10, 0, 0)

        return widget

    def loop_widget(self):
        """
        滚动内容
        :return:
        """
        # 创建滚动窗体
        widget = QScrollArea()

        # 创建滚动内容
        scroll_widget_content = QWidget()
        layout = QGridLayout(scroll_widget_content)

        # 创建滚动窗体内窗体
        scroll_widget_content.setObjectName('scroll_widget_content')
        scroll_widget_content.resize(380, 490)

        # 设置滚动窗体
        widget.setObjectName("dw_loop_widget")
        widget.setWidget(scroll_widget_content)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 设置属性
        widget.setWidgetResizable(True)

        # 获取控件
        dw_info: QWidget = path_page(self.font)

        # 添加控件
        layout.addWidget(dw_info, 1, 0, 1, 1, Qt.AlignTop)

        # 设置边距
        layout.setContentsMargins(0, 10, 10, 10)

        return widget

    def dw_title(self) -> QWidget:
        """
        标题控件
        :return:
        """
        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置控件属性
        widget.setObjectName("steam_set_title_widget")

        # 设置属性
        widget.setFixedSize(560, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        self.dw_title_label = QLabel('Steam设置')
        self.dw_title_label.setFont(QFont(self.font, 16))
        self.dw_title_label.setObjectName('title_label')
        layout.addWidget(self.dw_title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(10, 0, 0, 0)

        return widget


class DownloadWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("ui.other_widget", "DownloadWidget"),)

    # 静态方法available()，用于检查模块"core"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("ui.other_widget")

    # 静态方法create()，用于创建DownloadWidget类的实例，返回值为DownloadWidget对象。
    @staticmethod
    def create(create_type: [DownloadWidget]) -> DownloadWidget:
        return DownloadWidget()


add_creator(DownloadWidgetClassCreator)
