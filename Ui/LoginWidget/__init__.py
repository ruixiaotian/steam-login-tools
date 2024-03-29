#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 16:23
# @Author  : 桥话语权
# @File    : LoginWidget.py
# @Software: PyCharm
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)
from creart import add_creator, create, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Core.file_operation import FileOperation
from Ui.LoginWidget.AddUserCard import AddUserCard
from Ui.LoginWidget.ServerStateCard import ServerStateCard
from Ui.LoginWidget.UserInfoCard import (
    UserInfoCard,
    scroll_widget_card_setup,
)
from Ui.Share import shadow_setup


class LoginWidget:
    __file_operation = create(FileOperation)

    def __init__(self) -> None:
        self.pings = []

    def initialize(self, parent, font: str) -> None:
        self.parent = parent
        self.font = font

    def login_widget_setup(self) -> QWidget:
        """
        设置登录界面
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName("LoginWidget")

        # 获取控件
        create(ServerStateCard).initialize(self.parent, self.font, self.pings)
        create(AddUserCard).initialize(self.parent, self.font, self.refresh_widget)

        self.title_widget = self.__title_widget_setup()
        self.add_account_widget = create(AddUserCard).add_user_setup()
        self.server_status_widget = create(ServerStateCard).server_state_setup()
        account_info_widget = self.__account_info_widget_setup()
        # 添加控件
        layout.addWidget(self.title_widget, 0, 0, 1, 2)
        layout.addWidget(self.add_account_widget, 1, 0, 1, 1)
        layout.addWidget(self.server_status_widget, 1, 1, 1, 1)
        layout.addWidget(account_info_widget, 2, 0, 1, 2)

        return widget

    def __title_widget_setup(self) -> QWidget:
        """
        设置顶部标题的控件

        :return:
        """
        # 创建控件
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.setFixedSize(400, 50)
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # 添加控件
        label = QLabel("Login")
        label.setFont(QFont(self.font, 16))
        label.setObjectName("title_label")
        layout.addWidget(label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def __account_info_widget_setup(self):
        """
        设置账号信息的控件

        :param add_account_widget:
        :param server_status_widget:
        :return:
        """
        # 创建控件
        widget = QLabel()
        layout = QGridLayout(widget)

        # 右侧
        self.__account_info_widget_left()

        # 右侧
        create(UserInfoCard).initialize(widget, self.add_account_widget, self.server_status_widget)
        size_button = create(UserInfoCard).size_btn()
        fix_button = create(UserInfoCard).repair_btn()

        # 设置控件属性
        widget.resize(540, 230)
        widget.setObjectName("account_info_widget")

        # 添加控件
        layout.addWidget(self.scroll_widget, 0, 0, 3, 1)
        layout.addWidget(size_button, 0, 1, 1, 1, Qt.AlignTop)
        layout.addWidget(fix_button, 1, 1, 1, 1, Qt.AlignTop)

        layout.addItem(
            QSpacerItem(1, 500, QSizePolicy.Minimum, QSizePolicy.Maximum), 2, 1, 1, 1
        )

        layout.setVerticalSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        # 设置阴影
        shadow_setup(widget, (2, 3), 25, QColor(29, 190, 245, 80))

        return widget

    def __account_info_widget_left(self) -> QWidget:
        """设置又侧的滚动窗体控件"""
        # 创建滚动窗体
        self.scroll_widget = QScrollArea()
        self.scroll_widget.setObjectName("scroll_widget")
        self.scroll_widget.setWidgetResizable(True)

        # 创建滚动窗体内窗体
        self.scroll_widget_content = self.__loop_add_widget()
        self.scroll_widget_content.setObjectName("scroll_widget_content")
        self.scroll_widget_content.resize(535, 220)

        self.scroll_widget.setWidget(self.scroll_widget_content)

    def __loop_add_widget(self) -> QWidget:
        """
        循环添加控件
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        user_list: list = self.__file_operation.read_cammy_json()  # 读取账号信息
        for user, num in zip(user_list, range(len(user_list))):
            # 循环创建控件
            layout.addWidget(
                scroll_widget_card_setup(
                    user, self.font, self.refresh_widget, self.parent
                ),
                num,
                0,
                1,
                1,
                Qt.AlignTop,
            )

        layout.addItem(
            QSpacerItem(1000, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding),
            len(user_list) + 1,
            0,
            1,
            1,
        )

        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)

        return widget

    def refresh_widget(self):
        """
        刷新窗体
        :return:
        """
        self.scroll_widget_content = self.__loop_add_widget()
        self.scroll_widget_content.setObjectName("scroll_widget_content")
        self.scroll_widget_content.resize(540, 220)
        self.scroll_widget.setWidget(self.scroll_widget_content)


class LoginWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LoginWidget", "LoginWidget"),)

    # 静态方法available()，用于检查模块"LoginWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginWidget")

    # 静态方法create()，用于创建LoginWidget类的实例，返回值为LoginWidget对象。
    @staticmethod
    def create(create_type: [LoginWidget]) -> LoginWidget:
        return LoginWidget()


add_creator(LoginWidgetClassCreator)
