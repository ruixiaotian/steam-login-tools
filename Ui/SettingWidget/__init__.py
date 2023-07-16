"""
设置页面页面
"""
from abc import ABC
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPixmap
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)
from creart import add_creator, exists_module, create
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.SettingWidget.Card import (
    CommonCard,
    LoginCard,
    AuthorizationCard,
    AboutCard,
    QQCard,
    AddCard,
)
from Ui.Share import shadow_setup


class SettingWidget:
    def __init__(self) -> None:
        pass

    def initialize(self, parent: QMainWindow, font: str) -> None:
        self.parent = parent
        self.font = font

    def setting_widget_setup(self) -> QWidget:
        """设置界面"""
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName("SettingWidget")

        # 获取控件
        software_info_widget = self.software_info()
        software_setting_widget = self.software_setting()

        # 添加控件
        layout.addWidget(software_info_widget, 0, 0, 1, 1)
        layout.addWidget(software_setting_widget, 1, 0, 1, 1)

        return widget

    def software_info(self) -> QWidget:
        """软件信息控件"""
        # 创建基础控件，并设置属性
        self.soft_info_widget = QWidget(self.parent)
        layout = QGridLayout(self.soft_info_widget)

        # 设置最大高度
        self.soft_info_widget.setFixedHeight(160)

        # 设置对象名称，用于QSS定位
        self.soft_info_widget.setObjectName("author_info_widget")

        """创建子控件"""
        # 设置软件头像
        __img_path = Path("./img/SettingWidget/github.svg")
        __pixmap = QPixmap(64, 64)
        __pixmap.load(str(__img_path))
        img = QLabel()
        img.setObjectName("software_info_img")
        img.setPixmap(__pixmap)
        img.setFixedSize(64, 64)
        img.setScaledContents(True)

        #  软件名字
        title = QLabel("Steam Login Tools")
        title.setObjectName("software_info_title")
        title.setFont(QFont(self.font, 17))

        # 软件信息
        a = "<a style='text-decoration: none; color: #1DBEF5' href='https://github.com/ruixiaotian/steam-login-tools'>GitHub</a>"
        msg = QLabel(f"这是一个来自于 {a} 的开源项目 ")
        msg.setOpenExternalLinks(True)
        msg.setObjectName("software_info_msg")
        msg.setFont(QFont(self.font, 10))

        """添加到控件"""
        layout.setContentsMargins(40, 30, 35, 18)
        layout.addWidget(img, 0, 0, 4, 1, Qt.AlignLeft)
        layout.addItem(
            QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Minimum), 0, 0, 1, 1
        )
        layout.addWidget(title, 1, 1, 1, 1, Qt.AlignRight)
        layout.addWidget(msg, 2, 1, 1, 1, Qt.AlignRight)
        layout.addItem(
            QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0, 1, 1
        )

        # 添加阴影
        shadow_setup(self.soft_info_widget, (2, 2), 20, QColor(29, 190, 245, 60))

        return self.soft_info_widget

    def software_setting(self) -> QWidget:
        """软件设置控件"""
        # 创建基础控件，并设置属性
        self.soft_setting_widget = QWidget(self.parent)
        layout = QGridLayout(self.soft_setting_widget)
        # 设置最大高度
        self.soft_setting_widget.setFixedHeight(290)
        # 设置对象名称，用于QSS定位
        self.soft_setting_widget.setObjectName("software_setting_widget")

        """创建子控件"""
        create(CommonCard).initialize(self.font)
        create(LoginCard).initialize(self.font)
        create(AuthorizationCard).initialize(self.font)
        create(AboutCard).initialize(self.font)
        create(QQCard).initialize(self.font)
        create(AddCard).initialize(self.font)

        """添加到控件"""
        layout.addWidget(create(CommonCard), 0, 0, 1, 1)
        layout.addWidget(create(LoginCard), 0, 1, 1, 1)
        layout.addWidget(create(AuthorizationCard), 0, 2, 1, 1)
        layout.addWidget(create(AboutCard), 0, 3, 1, 1)
        layout.addWidget(create(QQCard), 1, 0, 1, 1)
        layout.addWidget(create(AddCard), 1, 1, 1, 1)

        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        # 添加阴影
        shadow_setup(self.soft_setting_widget, (2, 2), 20, QColor(29, 190, 245, 60))

        return self.soft_setting_widget


class SettingWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget", "SettingWidget"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget")

    # 静态方法create()，用于创建SettingWidget类的实例，返回值为SettingWidget对象。
    @staticmethod
    def create(create_type: [SettingWidget]) -> SettingWidget:
        return SettingWidget()


add_creator(SettingWidgetClassCreator)
