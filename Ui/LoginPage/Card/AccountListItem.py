#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :AccountListItem.py
# @Time :2023-8-18 下午 10:03
# @Author :Qiao
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QWidget

from qfluentwidgets.components import (
    SmoothScrollArea
)


class AccountCard(QFrame):
    """账号卡片"""

    def __init__(self, account: dict) -> None:
        """初始化"""
        super().__init__()


class AccountListView(SmoothScrollArea):
    """处理账号信息列表中的卡片展示"""

    def __init__(self, parent=None) -> None:
        """初始化"""
        super().__init__(parent=parent)

        # 关闭垂直和水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 为视图设定名称
        self.view.setObjectName("view")

        self.view = QWidget(self)  # 创建一个QWidget实例作为视图
        self.vBoxLayout = QVBoxLayout(self.view)  # 为视图设立水平布局

    def __setupLayouts(self) -> None:
        """私有方法，用于设置布局属性"""
        # 设置内容边距
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        # 设置间隔
        self.vBoxLayout.setSpacing(12)
        # 设置对齐方式
        self.vBoxLayout.setAlignment(Qt.AlignTop)
