"""
网络加速页面
"""
from abc import ABC
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QMainWindow, QWidget
from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo


class NetWidget:
    def __init__(self):
        pass

    def initialize(self, parent: QMainWindow, font: str):
        self.parent = parent
        self.font = font

    def net_widget_setup(self):
        """
        网络界面
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName("net_widget")

        # 获取控件
        img_path = Path("./img/icon/net/under_development.png")
        pixmap = QPixmap(128, 128)
        pixmap.load(str(img_path))

        img = QLabel()
        img.setPixmap(pixmap)
        img.setFixedSize(450, 450)
        img.setScaledContents(True)

        label = QLabel("这里的内容,以后再来探索吧")
        label.setFont(QFont(self.font, 13))

        # 添加控件
        layout.addWidget(img, 0, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(label, 1, 0, 1, 1, Qt.AlignCenter)

        return widget


class NetWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.NetWidget", "NetWidget"),)

    # 静态方法available()，用于检查模块"Ui.NetWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.NetWidget")

    # 静态方法create()，用于创建NetWidget类的实例，返回值为NetWidget对象。
    @staticmethod
    def create(create_type: [NetWidget]) -> NetWidget:
        return NetWidget()


add_creator(NetWidgetClassCreator)
