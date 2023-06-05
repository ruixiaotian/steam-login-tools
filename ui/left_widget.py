#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 22:49
# @Author  : 桥话语权
# @File    : left_widget.py
# @Software: PyCharm
"""
* 设置窗体左方的一些函数
"""
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMainWindow, QGridLayout, QListWidget, \
    QListWidgetItem, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSvg import QSvgRenderer
from core.event_judgment import list_widget_icon_color


def top_icon_setup(font: QFont) -> QWidget:
    """
    用于设置左上方Logo的函数
    :param font: 设置QLabel字体
    :return: QWidget
    """
    widget = QWidget()
    layout = QGridLayout(widget)
    # 窗体设置
    widget.setFixedSize(150, 100)

    # 创建 QSvgRenderer 对象并传入svg路径
    svg = QSvgRenderer("./img/icon/steam.svg")

    # 设置 QPixmap
    pixmap = QPixmap(42, 42)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    svg.render(painter)
    # 需要删除 painter 否则会引发 QPaintDevice: Cannot destroy paint device that is being painted 错误
    del painter

    # 把 QPixmap 贴到 QLabel 上
    logo_label = QLabel()
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignHCenter)

    # 设置文字 QLabel 内容
    word_label = QLabel("Steam Login")
    word_label.setObjectName("logo_word_label")
    word_label.setFont(font)
    word_label.setAlignment(Qt.AlignCenter)

    # 添加到布局
    layout.addWidget(logo_label, 0, 0, 1, 1, Qt.AlignCenter)
    layout.addWidget(word_label, 1, 0, 1, 1, Qt.AlignCenter)
    layout.setContentsMargins(0, 30, 0, 0)

    return widget


def left_button_setup(font: str, page_widget: QWidget) -> QWidget:
    """
    page_widget: QStackedWidget
    设置左方窗体的切换按钮等设置
    :param font: 设置QLabel字体
    :param page_widget: 右方切换窗体用于绑定按钮事件
    :return: QWidget
    """
    widget = QWidget()  # 创建承载控件
    layout = QGridLayout(widget)

    # 创建svg文件指向
    file_name_list = [
        "./img/icon/login_widget/item_icon/user.svg",
        "./img/icon/login_widget/item_icon/net_acceleration.svg",
        "./img/icon/login_widget/item_icon/fun_setting.svg"
    ]

    # 窗体设置
    widget.resize(140, 200)

    # 创建 QWidgetList 表格
    widget_list = QListWidget()
    widget_list.setFixedSize(130, 180)
    widget_list.setObjectName("left_widget_list")
    widget_list.setFont(font)

    # 创建item选项
    item_list = [
        QListWidgetItem(QIcon(file_name_list[0]), "账号登录"),
        QListWidgetItem(QIcon(file_name_list[1]), "网络加速"),
        QListWidgetItem(QIcon(file_name_list[2]), "功能设置"),
    ]

    # 循环设置控件
    for i in item_list:
        widget_list.addItem(i)
        i.setTextAlignment(Qt.AlignCenter)

    # 设置单独属性
    widget_list.setIconSize(QSize(24, 24))
    widget_list.setCurrentRow(0)
    # 绑定事件
    widget_list.currentItemChanged.connect(list_widget_icon_color)  # 绑定颜色切换事件
    widget_list.currentItemChanged.connect(
        lambda: page_widget.setCurrentIndex(widget_list.currentRow())
    )

    # 添加到布局
    layout.addWidget(widget_list, 0, 0, 1, 2)
    layout.setContentsMargins(0, 0, 0, 0)

    return widget


def left_label_setup(font: str, ui: QMainWindow) -> QWidget:
    """设置左下角版本号和退出按钮"""
    widget = QWidget()  # 创建承载控件
    layout = QGridLayout(widget)

    # 窗体设置
    widget.resize(60, 40)

    # 创建控件
    button = QPushButton("退出软件")
    label = QLabel("3.0.0_Beta")
    # 设置属性
    button.setFont(QFont(font, 8))
    label.setFont(QFont(font, 6))

    # 设置图标和对象名称
    button.setIcon(QIcon("./img/icon/login_widget/item_icon/exit.svg"))
    button.setObjectName("exit_button")
    label.setObjectName("version_label")

    # 绑定按钮事件
    button.clicked.connect(
        lambda: (
            ui.close()
            if ui.close_state else
            not ui.close_state
        )
    )

    # 添加到布局
    layout.addWidget(button, 0, 0, 1, 1, Qt.AlignLeft)
    layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum))
    layout.addWidget(label, 2, 0, 1, 1, Qt.AlignLeft)
    layout.setContentsMargins(0, 0, 0, 0)

    return widget
