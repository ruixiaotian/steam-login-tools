from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QWidget,
)
from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.OtherWidget.FixLoginWidget.FixPage import fix_page as fix_page_widget
from Ui.OtherWidget.FixLoginWidget.info_page import info_page as info_page_widget


class FixLoginWidget:
    def __init__(self) -> None:
        pass

    def initialize(self, parent: QMainWindow, font: str, page: QStackedWidget) -> None:
        self.parent = parent
        self.font = font
        self.page = page

    def fix_widget_setup(self) -> QWidget:
        """
        设置页面
        :return:
        """
        # 创建页面
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(390, 500)
        widget.setObjectName("other_page_widget")

        # 添加到布局
        layout.addWidget(self.fix_title(), 1, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.loop_widget(), 2, 0, 1, 1)

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
        widget.setObjectName("other_page_title_widget")

        # 设置属性
        widget.setFixedSize(560, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        self.title_label = QLabel("修复登录错误")
        self.title_label.setFont(QFont(self.font, 16))
        self.title_label.setObjectName("title_label")

        self.return_btn = QPushButton()
        self.return_btn.setIcon(
            QIcon("./img/OtherWidget/share/other_page_return_btn.svg")
        )
        self.return_btn.setObjectName("other_page_return_btn")
        self.return_btn.clicked.connect(lambda: self.page.setCurrentIndex(0))

        layout.addWidget(self.title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.return_btn, 0, 1, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        layout.setContentsMargins(10, 5, 15, 10)

        return widget

    def loop_widget(self) -> QWidget:
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
        scroll_widget_content.setObjectName("scroll_widget_content")
        scroll_widget_content.resize(380, 490)

        # 设置滚动窗体
        widget.setObjectName("other_page_loop_widget")
        widget.setWidget(scroll_widget_content)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 设置属性
        widget.setWidgetResizable(True)

        # 获取控件
        info_page = info_page_widget(self.font)
        fix_page = fix_page_widget(self.font, self.parent)

        # 添加控件
        layout.addWidget(info_page, 0, 0, 1, 1)
        layout.addWidget(fix_page, 1, 0, 1, 1)
        layout.addItem(
            QSpacerItem(1, 1000, QSizePolicy.Minimum, QSizePolicy.Maximum), 2, 0, 1, 1
        )

        # 设置边距
        layout.setContentsMargins(0, 10, 10, 10)
        layout.setVerticalSpacing(0)

        return widget


class FixLoginWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.OtherWidget.FixLoginWidget", "FixLoginWidget"),)

    # 静态方法available()，用于检查模块"FixLoginWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.OtherWidget.FixLoginWidget")

    # 静态方法create()，用于创建FixLoginWidget类的实例，返回值为FixLoginWidget对象。
    @staticmethod
    def create(create_type: [FixLoginWidget]) -> FixLoginWidget:
        return FixLoginWidget()


add_creator(FixLoginWidgetClassCreator)
