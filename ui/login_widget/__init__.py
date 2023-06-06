#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 16:23
# @Author  : 桥话语权
# @File    : login_widget.py
# @Software: PyCharm

import json
import datetime

import loguru
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QCheckBox, QAction, \
    QSizePolicy, QGraphicsDropShadowEffect, QScrollArea, QMenu, QSpacerItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QMouseEvent, QCloseEvent
from PyQt5.QtCore import Qt, QPropertyAnimation
from pathlib import Path

from core.file_operation import FileOperation
from core.network_threads import PingServerThread, SteamLoginThread
from core.event_judgment import login_widget_size_button_checked_event

from ui.share import shadow_setup
from ui.other_widget import DownloadWidget
from ui.login_widget.add_act_wgt_set import add_account_widget_setup
from ui.login_widget.server_status_wgt_set import server_status_widget_setup
from ui.login_widget.act_info_wgt_set import scroll_widget_card_setup

from creart import create


class LoginWidget:
    __file_operation = create(FileOperation)

    def __init__(self, parent, font: str):
        self.parent = parent
        self.font = font
        self.pings = list()

    def login_widget_setup(self, ui: QMainWindow):
        """
        设置登录界面
        :param ui:
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName('login_widget')

        # 获取控件
        title_widget = self.__title_widget_setup()
        add_account_widget = add_account_widget_setup(self.font, self.__refresh_widget)
        server_status_widget = server_status_widget_setup(self.font, ui, self.pings)
        account_info_widget = self.__account_info_widget_setup(add_account_widget, server_status_widget)
        # 添加控件
        layout.addWidget(title_widget, 0, 0, 1, 2)
        layout.addWidget(add_account_widget, 1, 0, 1, 1)
        layout.addWidget(server_status_widget, 1, 1, 1, 1)
        layout.addWidget(account_info_widget, 2, 0, 1, 2)

        return widget

    def __title_widget_setup(self):
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
        label = QLabel('Login')
        label.setFont(QFont(self.font, 16))
        label.setObjectName('title_label')
        layout.addWidget(label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        return widget

    def __account_info_widget_setup(
            self, add_account_widget, server_status_widget
    ):
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
        size_button = self.__account_info_widget_right_size_btn(
            widget, add_account_widget, server_status_widget
        )
        dw_button = self.__account_info_widget_right_dw_btn()

        # 设置控件属性
        widget.resize(540, 230)
        widget.setObjectName('account_info_widget')

        # 添加控件
        layout.addWidget(self.scroll_widget, 0, 0, 3, 1)
        layout.addWidget(size_button, 0, 1, 1, 1, Qt.AlignTop)
        # layout.addWidget(dw_button, 1, 1, 1, 1, Qt.AlignTop)
        layout.addItem(QSpacerItem(1, 1000, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 1, 1, 1)

        # 设置阴影
        shadow_setup(widget, (2, 3), 25, QColor(29, 190, 245, 80))

        return widget

    @staticmethod
    def __account_info_widget_right_size_btn(
            widget, add_account_widget, server_status_widget
    ) -> QCheckBox:
        """
        设置右侧的放大/缩小控件
        :param widget:  承载窗体
        :param add_account_widget:  添加账号的控件
        :param server_status_widget:  服务器状态的控件
        :return:
        """
        size_button = QCheckBox()

        # 单独设置属性
        # 放大_缩小按钮设置, 绑定事件
        size_button.setObjectName('size_button')
        size_button.setFixedSize(32, 32)
        # int类型 当选中时为2,未选中时为0
        size_button.stateChanged.connect(
            lambda state:
            login_widget_size_button_checked_event(
                state, widget, add_account_widget, server_status_widget
            )
        )

        return size_button

    @staticmethod
    def __account_info_widget_right_dw_btn() -> QPushButton:
        """
        设置右侧下载旧版Steam文件按钮
        :return:
        """
        # 创建按钮
        dw_button = QCheckBox()

        # 下载按钮属性设置
        dw_button.setObjectName("dw_button")
        dw_button.setFixedSize(32, 32)

        # 信号绑定
        dw_button.stateChanged.connect(
            lambda:
            create(DownloadWidget).page.setCurrentIndex(3)
        )

        return dw_button

    def __account_info_widget_left(self) -> QWidget:
        """设置左侧的滚动窗体控件"""
        # 创建滚动窗体
        self.scroll_widget = QScrollArea()
        self.scroll_widget.setObjectName('scroll_widget')
        self.scroll_widget.setWidgetResizable(True)

        # 创建滚动窗体内窗体
        self.scroll_widget_content = self.__loop_add_widget()
        self.scroll_widget_content.setObjectName('scroll_widget_content')
        self.scroll_widget_content.resize(540, 220)

        self.scroll_widget.setWidget(self.scroll_widget_content)

    def __loop_add_widget(self) -> QWidget:
        """
        循环添加控件
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        account: list = self.__file_operation.read_cammy_json()  # 读取账号信息
        for i, num in zip(account, range(len(account))):
            # 循环创建控件
            layout.addWidget(scroll_widget_card_setup(i, self.font, self.__refresh_widget), num, 0, 1, 1, Qt.AlignTop)

        layout.addItem(
            QSpacerItem(1000, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding),
            len(account) + 1, 0, 1, 1
        )

        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)

        return widget

    def __refresh_widget(self):
        """
        刷新窗体
        :return:
        """
        self.scroll_widget_content = self.__loop_add_widget()
        self.scroll_widget_content.setObjectName('scroll_widget_content')
        self.scroll_widget_content.resize(540, 220)
        self.scroll_widget.setWidget(self.scroll_widget_content)
