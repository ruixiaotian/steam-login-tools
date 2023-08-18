#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-8-17 下午 10:58
# @Author :Qiao
from abc import ABC

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets.components import ScrollArea
from creart import add_creator, exists_module, create
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.HomePage.BannerWidget import BannerWidget
from Ui.StyleSheet import HomePageStyleSheet


class HomeWidget(ScrollArea):
    """Home Widget"""

    def __init__(self, parent=None):
        """初始化"""
        super().__init__(parent=parent)

    def initialize(self, parent):
        """初始化"""
        self.parentClass = parent
        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.view.setObjectName("view")
        self.setObjectName("homeInterface")
        HomePageStyleSheet.HOME_WIDGET.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)


class HomeWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.HomePage", "HomeWidget"),)

    # 静态方法available()，用于检查模块"HomeWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.HomePage")

    # 静态方法create()，用于创建HomeWidget类的实例，返回值为HomeWidget对象。
    @staticmethod
    def create(create_type: [HomeWidget]) -> HomeWidget:
        return HomeWidget()


add_creator(HomeWidgetClassCreator)
