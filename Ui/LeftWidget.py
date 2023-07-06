#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 22:49
# @Author  : 桥话语权
# @File    : LeftWidget.py
# @Software: PyCharm
from abc import ABC

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)
from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Core.EventJudgment import leftIconColor


class LeftWidget:
    def initialize(self, font: str, page_widget: QWidget, base_widget: QWidget):
        """初始化函数"""
        self.font = font
        self.page_widget = page_widget
        self.base_widget = base_widget

    def top_icon_setup(self) -> QWidget:
        """用于设置左上方Logo的函数"""
        widget = QWidget()
        layout = QGridLayout(widget)
        # 窗体设置
        widget.setFixedSize(150, 100)

        # 加载 Logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("./img/icon/steam.svg"))
        logo_label.setScaledContents(True)
        logo_label.setAlignment(Qt.AlignHCenter)

        # 设置文字 QLabel 内容
        word_label = QLabel("Steam Login Tools")
        word_label.setObjectName("logo_word_label")
        word_label.setFont(QFont(self.font, 11))
        word_label.setAlignment(Qt.AlignCenter)

        # 添加到布局
        layout.addWidget(logo_label, 0, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(word_label, 1, 0, 1, 1, Qt.AlignCenter)
        layout.setContentsMargins(0, 30, 0, 0)

        return widget

    def left_button_setup(self) -> QWidget:
        """设置左方窗体的切换按钮等设置"""
        widget = QWidget()  # 创建承载控件
        layout = QGridLayout(widget)

        # 创建svg文件指向
        file_name_list = [
            "./img/icon/LoginWidget/item_icon/user.svg",
            "./img/icon/LoginWidget/item_icon/net_acceleration.svg",
            "./img/icon/LoginWidget/item_icon/fun_setting.svg",
        ]

        # 窗体设置
        widget.resize(140, 200)

        # 创建 QWidgetList 表格
        widget_list = QListWidget()
        widget_list.setFixedSize(130, 180)
        widget_list.setObjectName("left_widget_list")
        widget_list.setFont(QFont(self.font, 13))

        # 创建item选项
        item_list = [
            QListWidgetItem(QIcon(file_name_list[0]), "账号登录"),
            QListWidgetItem(QIcon(file_name_list[1]), "网络加速"),
            QListWidgetItem(QIcon(file_name_list[2]), "功能设置"),
        ]

        # 循环设置控件
        _ = [widget_list.addItem(item) for item in item_list]
        _ = [item.setTextAlignment(Qt.AlignCenter) for item in item_list]

        # 设置单独属性
        widget_list.setIconSize(QSize(24, 24))
        widget_list.setCurrentRow(0)
        # 绑定事件
        widget_list.currentItemChanged.connect(leftIconColor)  # 绑定颜色切换事件
        widget_list.currentItemChanged.connect(
            lambda: self.page_widget.setCurrentIndex(widget_list.currentRow())
        )

        # 添加到布局
        layout.addWidget(widget_list, 0, 0, 1, 2)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def left_label_setup(self) -> QWidget:
        """设置左下角版本号和退出按钮"""
        widget = QWidget()  # 创建承载控件
        layout = QGridLayout(widget)

        # 窗体设置
        widget.resize(60, 40)

        # 创建控件
        button = QPushButton("退出软件")
        label = QLabel("3.0.0.10_Beta")
        # 设置属性
        button.setFont(QFont(self.font, 8))
        label.setFont(QFont(self.font, 6))

        # 设置图标和对象名称
        button.setIcon(QIcon("./img/icon/LoginWidget/item_icon/exit.svg"))
        button.setObjectName("exit_button")
        label.setObjectName("version_label")

        # 绑定按钮事件
        button.clicked.connect(
            lambda: (
                self.base_widget.close()
                if self.base_widget.close_state
                else not self.base_widget.close_state
            )
        )

        # 添加到布局
        layout.addWidget(button, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum))
        layout.addWidget(label, 2, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget


class LeftWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LeftWidget", "LeftWidget"),)

    # 静态方法available()，用于检查模块"Ui.LeftWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LeftWidget")

    # 静态方法create()，用于创建LeftWidget类的实例，返回值为LeftWidget对象。
    @staticmethod
    def create(create_type: [LeftWidget]) -> LeftWidget:
        return LeftWidget()


add_creator(LeftWidgetClassCreator)
