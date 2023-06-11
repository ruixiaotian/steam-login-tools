from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, \
    QSizePolicy, QScrollArea, QStackedWidget, QSpacerItem, QPushButton
from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from ui.other_widget.BulkImportWidget.info_page import info_page
from ui.other_widget.BulkImportWidget.txt_page import txt_page


class BulkImportWidget:

    def __init__(self):
        pass

    def initialize(self, parent: QMainWindow, font: str, page: QStackedWidget):
        self.parent = parent
        self.font = font
        self.page = page

    def bulk_import_widget_setup(self):
        """
        设置页面
        :return:
        """
        # 创建页面
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(390, 500)
        widget.setObjectName('other_page_widget')

        # 添加到布局
        layout.addWidget(self.bulk_import_title(), 1, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.loop_widget(), 2, 0, 1, 1)

        layout.setContentsMargins(0, 10, 0, 0)

        return widget

    def bulk_import_title(self) -> QWidget:
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
        self.title_label = QLabel('批量导入账号')
        self.title_label.setFont(QFont(self.font, 16))
        self.title_label.setObjectName('title_label')

        self.return_btn = QPushButton()
        self.return_btn.setIcon(QIcon("./img/other_widget/share/other_page_return_btn.svg"))
        self.return_btn.setObjectName("other_page_return_btn")
        self.return_btn.clicked.connect(lambda: self.page.setCurrentIndex(0))

        layout.addWidget(self.title_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.return_btn, 0, 1, 1, 1, Qt.AlignRight | Qt.AlignBottom)
        layout.setContentsMargins(10, 5, 15, 10)

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
        widget.setObjectName("other_page_loop_widget")
        widget.setWidget(scroll_widget_content)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条

        # 设置属性
        widget.setWidgetResizable(True)

        # 添加控件
        # layout.addWidget(info_page(self.font))
        layout.addWidget(txt_page(self.font), 0, 0, 1, 1)
        layout.addItem(QSpacerItem(1, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0, 1, 1)

        # 设置边距
        layout.setContentsMargins(0, 0, 10, 10)
        layout.setVerticalSpacing(0)

        return widget


class BulkImportWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("ui.other_widget.BulkImportWidget", "BulkImportWidget"),)

    # 静态方法available()，用于检查模块"BulkImportWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("ui.other_widget.BulkImportWidget")

    # 静态方法create()，用于创建BulkImportWidget类的实例，返回值为BulkImportWidget对象。
    @staticmethod
    def create(create_type: [BulkImportWidget]) -> BulkImportWidget:
        return BulkImportWidget()


add_creator(BulkImportWidgetClassCreator)
