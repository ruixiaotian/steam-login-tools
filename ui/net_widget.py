"""
网络加速页面
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path


class NetWidget:

    def __init__(self, parent: QMainWindow, font: str):
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
        widget.setObjectName('net_widget')

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
