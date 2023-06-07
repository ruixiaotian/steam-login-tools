from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, \
    QSizePolicy, QScrollArea, QStackedWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt

from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo
from abc import ABC

from core.file_operation import FileOperation
from ui.other_widget.FixLoginWidget.info_page import (
    info_page as info_page_widget
)

from creart import create


class FixLoginWidget:

    def __init__(self):
        pass

    def initialize(self, parent: QMainWindow, font: str, page: QStackedWidget):
        self.parent = parent
        self.font = font
        self.page = page

    def fix_widget_setup(self):
        """
        设置页面
        :return:
        """
        # 创建页面
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(390, 500)
        widget.setObjectName('dw_widget')

        # 添加到布局
        layout.addWidget(self.fix_title(), 1, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.loop_widget(), 2, 0, 1, 1, Qt.AlignTop)

        layout.setContentsMargins(0, 10, 0, 0)

        return widget

    def fix_title(self) -> QWidget:
        """
        标题控件
        :return:
        """
        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置控件属性
        widget.setObjectName("fix_login_title_widget")

        # 设置属性
        widget.setFixedSize(560, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        self.dw_title_label = QLabel('修复登录错误')
        self.dw_title_label.setFont(QFont(self.font, 16))
        self.dw_title_label.setObjectName('title_label')
        layout.addWidget(self.dw_title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(10, 0, 0, 0)

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
        widget.setObjectName("fix_loop_widget")
        widget.setWidget(scroll_widget_content)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 设置属性
        widget.setWidgetResizable(True)

        # 获取控件
        info_page = info_page_widget(self.font)

        # 添加控件
        layout.addWidget(info_page, 0, 0, 1, 1)

        # 设置边距
        layout.setContentsMargins(0, 10, 10, 10)

        return widget


class FixLoginWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("ui.other_widget.FixLoginWidget", "FixLoginWidget"),)

    # 静态方法available()，用于检查模块"FixLoginWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("ui.other_widget.FixLoginWidget")

    # 静态方法create()，用于创建FixLoginWidget类的实例，返回值为FixLoginWidget对象。
    @staticmethod
    def create(create_type: [FixLoginWidget]) -> FixLoginWidget:
        return FixLoginWidget()


add_creator(FixLoginWidgetClassCreator)