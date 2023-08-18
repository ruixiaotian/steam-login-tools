#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :BannerWidget.py
# @Time :2023-8-17 下午 11:42
# @Author :Qiao
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets.common import FluentIcon, isDarkTheme

from Core.config import HELP_URL, REPO_URL, QQ_GROUP_URL, FEEDBACK_URL
from Ui.HomePage.LinkCard import LinkCardView


class BannerWidget(QWidget):
    """主页上方的 Banner widget"""

    def __init__(self, parent=None) -> None:
        """初始化"""
        super().__init__(parent=parent)

        self.setObjectName("SteamLoginToolsLabel")
        self.createChildControls()
        self.setupAttribute()
        self.addCard()
        self.setupLayout()

    def setupAttribute(self) -> None:
        """设置控件的属性"""
        self.setFixedHeight(336)
        self.toolsLabel.setObjectName("galleryLabel")

    def createChildControls(self) -> None:
        """创建子控件"""
        self.toolsLabel = QLabel("Steam Login Tools", self)
        self.banner = QPixmap(":HomePage/image/HomePage/header_white.png")
        self.linkCardView = LinkCardView(self)

    def setupLayout(self) -> None:
        """设置Layout"""
        # 创建一个布局
        self.vBoxLayout = QVBoxLayout(self)

        # 设置布局属性
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.toolsLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def addCard(self) -> None:
        """添加卡片"""
        self.linkCardView.addCard(
            icon=":MainWindow/image/MainWindow/Logo_white.svg",
            title=self.tr("What is it?"),
            content=self.tr("This is a Steam account management tools."),
            url=HELP_URL,
        )
        self.linkCardView.addCard(
            icon=FluentIcon.GITHUB,
            title=self.tr("GitHub repo"),
            content=self.tr(
                "This is an open source project based on the GPLv3 license."
            ),
            url=REPO_URL,
        )
        self.linkCardView.addCard(
            icon=FluentIcon.ADD,
            title=self.tr("Discuss"),
            content=self.tr("Join the QQ group discussion."),
            url=QQ_GROUP_URL,
        )
        self.linkCardView.addCard(
            icon=FluentIcon.FEEDBACK,
            title=self.tr("Send feedback"),
            content=self.tr("Improve Steam Login Tools with feedback."),
            url=FEEDBACK_URL,
        )

    def paintEvent(self, e) -> None:
        """paintEvent方法用于绘制部件的外观"""
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing
        )
        painter.setPen(Qt.NoPen)

        # 创建路径和形状
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), 200
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # 根据主题绘制背景颜色
        if not isDarkTheme():
            painter.fillPath(path, QColor(206, 216, 228))
        else:
            painter.fillPath(path, QColor(0, 0, 0))

        # 绘制 banner 图像
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation
        )
        path.addRect(QRectF(0, h, w, self.height() - h))
        painter.fillPath(path, QBrush(pixmap))
