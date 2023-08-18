#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :LinkCard.py
# @Time :2023-8-17 下午 11:12
# @Author :Qiao
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from qfluentwidgets import IconWidget, FluentIcon, TextWrap, SingleDirectionScrollArea

from Ui.StyleSheet import HomePageStyleSheet


class LinkCard(QFrame):
    def __init__(self, icon, title, content, url, parent=None) -> None:
        """初始化"""
        super().__init__(parent=parent)
        self.url = QUrl(url)
        self.setFixedSize(198, 220)

        # 创建子控件
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 28, False)[0], self)
        self.urlWidget = IconWidget(FluentIcon.LINK, self)

        self.__initWidget()

    def __initWidget(self) -> None:
        """初始化控件"""
        self.setCursor(Qt.PointingHandCursor)

        self.__setupWidgets()
        self.__setupLayouts()

    def __setupWidgets(self) -> None:
        """设置控件"""
        self.iconWidget.setFixedSize(54, 54)
        self.urlWidget.setFixedSize(16, 16)
        self.urlWidget.move(170, 192)

        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

    def __setupLayouts(self) -> None:
        """设置Layout"""
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def mouseReleaseEvent(self, event) -> None:
        """重构事件实现点击效果"""
        super().mouseReleaseEvent(event)
        QDesktopServices.openUrl(self.url)


class LinkCardView(SingleDirectionScrollArea):
    """LinkCardView类，处理链接卡片的展示，继承自SingleDirectionScrollArea"""

    def __init__(self, parent=None) -> None:
        """初始化"""
        super().__init__(parent, Qt.Horizontal)

        self.view = QWidget(self)  # 创建一个QWidget实例作为视图
        self.hBoxLayout = QHBoxLayout(self.view)  # 为视图设立水平布局

        self.__setupLayouts()  # 调用内部方法对布局进行设置

        # 设置窗体小部件和调整大小属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        # 关闭垂直和水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 为视图设定名称
        self.view.setObjectName("view")

        # 使用样式表修改LinkCardView的外观
        HomePageStyleSheet.LINK_CARD.apply(self)

    def __setupLayouts(self) -> None:
        """私有方法，用于设置布局属性"""
        # 设置内容边距
        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        # 设置间隔
        self.hBoxLayout.setSpacing(12)
        # 设置对齐方式
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

    def addCard(self, icon, title, content, url) -> None:
        """添加新的链接卡片"""
        # 创建LinkCard实例
        card = LinkCard(icon, title, content, url, self.view)

        # 将新建的卡片添加到布局中，以左对齐的方式
        self.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)
