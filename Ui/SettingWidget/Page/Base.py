#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :BasePage.py
# @Time :2023-7-17 下午 03:57
# @Author :Qiao
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QSizePolicy,
    QPushButton,
    QScrollArea,
    QSpacerItem,
)

from Ui.Share import shadow_setup


class SettingWidgetBase(QWidget):
    font: str | None
    page: None
    parent: None
    title_content: str | None
    scroll_content: list | None

    def __init__(self):
        super().__init__()
        self.scroll_content = []

    def setupLayout(self):
        """设置布局"""
        self.resize(390, 500)
        self.setObjectName("setting_page_widget")

        # 创建布局,并添加控件
        layout = QGridLayout()
        layout.addWidget(self.setupTitle(), 1, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.setupLoopWidget(), 2, 0, 1, 1)

        layout.setContentsMargins(0, 10, 0, 0)

        self.setLayout(layout)

    def setupTitle(self):
        """标题控件"""
        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置控件属性
        widget.setObjectName("setting_page_title_widget")

        # 设置属性
        widget.setFixedSize(560, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        self.title_label = QLabel(self.title_content)
        self.title_label.setFont(QFont(self.font, 16))
        self.title_label.setObjectName("title_label")

        self.return_btn = QPushButton()
        self.return_btn.setIcon(
            QIcon("./img/SettingWidget/share/setting_page_return_btn.svg")
        )
        self.return_btn.setObjectName("setting_page_return_btn")
        self.return_btn.clicked.connect(lambda: self.page.setCurrentIndex(2))

        layout.addWidget(self.title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.return_btn, 0, 1, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        layout.setContentsMargins(10, 5, 15, 10)

        return widget

    def setupLoopWidget(self) -> QWidget:
        """滚动内容"""
        # 创建滚动窗体
        widget = QScrollArea()

        # 创建滚动内容
        scroll_widget_content = QWidget()
        self.scroll_widget_layout = QGridLayout(scroll_widget_content)

        # 创建滚动窗体内窗体
        scroll_widget_content.setObjectName("scroll_widget_content")
        scroll_widget_content.resize(380, 490)

        # 设置滚动窗体
        widget.setObjectName("setting_page_loop_widget")
        widget.setWidget(scroll_widget_content)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条
        widget.setWidgetResizable(True)

        # 添加控件
        for num, i in enumerate(self.scroll_content):
            self.scroll_widget_layout.addWidget(i, num, 0, 1, 1)
        self.scroll_widget_layout.addItem(
            QSpacerItem(1, 100, vPolicy=QSizePolicy.Expanding),
            len(self.scroll_content) + 1, 0, 1, 1,
        )

        # 设置边距
        self.scroll_widget_layout.setContentsMargins(0, 0, 10, 10)
        self.scroll_widget_layout.setVerticalSpacing(0)

        return widget


class CardBase(QWidget):
    """页面内卡片的基类"""

    font: str
    title_content: str | None
    card_height: int | None

    def __init__(self):
        super().__init__()

    def setupLayout(self):
        """设置布局"""
        layout = QGridLayout()
        layout.addWidget(self.setupTitle(), 0, 0, 1, 1)
        layout.addWidget(self.setupCard(), 1, 0, 1, 1)
        layout.setVerticalSpacing(0)

        self.setLayout(layout)

    def setupTitle(self):
        """设置标题"""
        title_widget = QWidget()
        title_layout = QGridLayout(title_widget)
        self.title = QLabel(self.title_content)
        self.title.setFont(QFont(self.font, 10))
        self.title.setObjectName("setting_page_min_title_label")

        title_layout.addWidget(self.title)
        title_layout.setContentsMargins(30, 0, 0, 0)
        title_layout.setVerticalSpacing(1)

        return title_widget

    def setupCard(self):
        """设置卡片"""
        self.card_widget = QWidget()
        self.card_widget_layout = QGridLayout(self.card_widget)
        # 设置属性
        self.card_widget.setFixedHeight(185)
        self.card_widget.setObjectName("card_widget")

        # 添加阴影
        shadow_setup(self.card_widget, (2, 2), 10, QColor(29, 190, 245, 60))

        return self.card_widget
