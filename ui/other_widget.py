import json
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
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName('dw_widget')

        # 获取控件
        dw_title: QWidget = self.dw_title()
        dw_info: QWidget = self.dw_info_widget()

        # 添加控件
        layout.addWidget(dw_title, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(dw_info, 1, 0, 1, 1, Qt.AlignTop)
        # layout.addItem(QSpacerItem(10, 100, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 0, 1, 1)

        # 设置边距
        layout.setContentsMargins(10, 10, 10, 10)

        return widget

    def dw_title(self) -> QWidget:
        """
        标题控件
        :return:
        """
        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.setFixedSize(400, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        self.dw_title_label = QLabel('Steam设置')
        self.dw_title_label.setFont(QFont(self.parent.font_name, 16))
        self.dw_title_label.setObjectName('title_label')
        layout.addWidget(self.dw_title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def dw_info_widget(self) -> QWidget:
        """
        下载信息控件
        :return:
        """
        # 创建基础控件，并设置属性
        self.dw_info_widget = QWidget(self.parent)
        layout = QGridLayout(self.dw_info_widget)

        # 设置最大高度
        self.dw_info_widget.setFixedHeight(185)

        # 设置对象名称，用于QSS定位
        self.dw_info_widget.setObjectName("author_info_widget")

        """创建子控件"""
        new_steam_path = self.dw_info_widget_new_steam_path()
        old_steam_path = self.dw_info_widget_old_steam_path()

        """添加到控件"""
        layout.addWidget(new_steam_path, 0, 0, 1, 1)
        layout.addWidget(old_steam_path, 1, 0, 1, 1)
        # layout.setContentsMargins(30, 20, 30, 15)

        # 添加阴影
        self.shadow_setup(self.dw_info_widget)

        return self.dw_info_widget

    def dw_info_widget_new_steam_path(self):
        """
        旧版steam路径
        :return:
        """
        """构建控件"""

        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置控件属性
        # widget.setFixedSize(260, 25)

        # 创建子控件
        label = QLabel("新版Steam路径：")
        edit = QLineEdit("未检测到路径")
        button = QPushButton(
            QIcon("./img/other_widget/dw/choose_file.svg"),
            "手动选择"
        )

        # 创建子控件列表
        widget_list = [label, edit, button]

        # 设置控件属性
        label.setObjectName("steam_path_label")
        edit.setObjectName("steam_path_edit")
        button.setObjectName("steam_path_button")

        # 设置共有属性
        for i in widget_list:
            i.setFont(QFont(self.parent.font_name, 10))

        # 设置label独有属性
        label.setFixedSize(100, 20)

        # 设置edit独有属性
        edit.setFixedSize(280, 20)
        edit.setReadOnly(True)  # 设置只读

        # 设置button独有属性
        button.setFixedSize(75, 20)
        button.setIconSize(QSize(14, 14))

        # 添加到控件
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(edit, 0, 1, 1, 1)
        layout.addWidget(button, 0, 2, 1, 1)
        layout.setContentsMargins(20, 5, 20, 5)

        """功能实现"""
        # 读取配置文件中的新版Steam路径
        if not create(FileOperation).config_data["steam_set"]["path"]["new"] is None:
            edit.setText(create(FileOperation).steam_path.__str__().capitalize())

        return widget

    def dw_info_widget_old_steam_path(self):
        """
        旧版steam路径
        :return:
        """
        """构建控件"""

        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置控件属性
        # widget.setFixedSize(260, 25)

        # 创建子控件
        label = QLabel("旧版Steam路径：")
        edit = QLineEdit("未检测到路径")
        button = QPushButton(
            QIcon("./img/other_widget/dw/choose_file.svg"),
            "手动选择"
        )

        # 创建子控件列表
        widget_list = [label, edit, button]

        # 设置控件属性
        label.setObjectName("steam_path_label")
        edit.setObjectName("steam_path_edit")
        button.setObjectName("steam_path_button")

        # 设置共有属性
        for i in widget_list:
            i.setFont(QFont(self.parent.font_name, 10))

        # 设置label独有属性
        label.setFixedSize(100, 20)

        # 设置edit独有属性
        edit.setFixedSize(280, 20)
        edit.setReadOnly(True)  # 设置只读

        # 设置button独有属性
        button.setFixedSize(75, 20)
        button.setIconSize(QSize(14, 14))

        # 添加到控件
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(edit, 0, 1, 1, 1)
        layout.addWidget(button, 0, 2, 1, 1)
        layout.setContentsMargins(20, 5, 20, 5)

        """功能实现"""

        # 读取配置文件中的旧版Steam路径
        if create(FileOperation).config_data["steam_set"]["path"]["old"] is None:
            edit.setText("未下载旧版Steam")

        return widget

    @staticmethod
    def shadow_setup(target: QWidget):
        # 设置阴影
        effect_shadow = QGraphicsDropShadowEffect(target)  # 创建阴影效果对象
        effect_shadow.setOffset(2, 3)  # 阴影的偏移量
        effect_shadow.setBlurRadius(25)  # 阴影的模糊程度
        effect_shadow.setColor(QColor(29, 190, 245, 80))  # 阴影的颜色
        target.setGraphicsEffect(effect_shadow)  # 设置阴影效果


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
