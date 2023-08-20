#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :AccountListItem.py
# @Time :2023-8-18 下午 10:03
# @Author :Qiao
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QWidget,
)
from qfluentwidgets.common import Action, FluentIcon
from qfluentwidgets.components import (
    SmoothScrollArea,
    ImageLabel,
    CheckableMenu,
    MenuAnimationType,
)

from Ui.StyleSheet import LoginPageStyleSheet


class AccountCard(QFrame):
    """账号卡片"""

    def __init__(self, account: dict) -> None:
        """初始化"""
        super().__init__()
        self.user = account["User"]
        self.password = account["PassWord"]
        self.ssfn = account["SSFN"]
        self.timeStamp = account["Timestamp"]
        self.skipEmail = account["SkipEmail"]
        self.steamId = account["SteamId"]

        # 创建子控件
        self.__setupAvatar()
        self.remarkLabel = QLabel(self.user, self)
        self.userLabel = QLabel("*" * 30, self)
        self.timeLabel = QLabel(self.tr("Not logged in yet"), self)

        self.__setupWidgets()
        self.__setupLayout()

    def __setupWidgets(self) -> None:
        """设置控件"""
        self.setFixedHeight(150)
        # 设置对象名称
        self.remarkLabel.setObjectName("remarkLabel")
        self.userLabel.setObjectName("userLabel")
        self.timeLabel.setObjectName("timeLabel")

    def __setupAvatar(self):
        """设置头像"""
        if self.steamId is None:
            self.iconLabel = QLabel("?", self)
            self.iconLabel.setObjectName("iconLabel")
            self.iconLabel.setFixedSize(150, 148)
            self.iconLabel.setAlignment(Qt.AlignCenter)
        else:
            self.iconLabel = ImageLabel(self)

    def contextMenuEvent(self, event: QContextMenuEvent):
        """设置菜单"""
        self.menu = CheckableMenu(parent=self)

        # 创建菜单项
        self.showUserAction = Action(FluentIcon.HIDE, self.tr("Show User Name"))
        self.showLoginBtn = Action(self.tr("Show Login Button"))
        self.SkipEmailBtn = Action(self.tr("Skip Email Validation"))

        # 链接槽函数
        self.showUserAction.triggered.connect(self.__showUserTrough)

        # 添加到菜单
        self.menu.addAction(self.showUserAction)
        self.menu.addAction(self.showLoginBtn)
        self.menu.addAction(self.SkipEmailBtn)

        self.menu.exec(event.globalPos(), ani=True, aniType=MenuAnimationType.DROP_DOWN)

    def __setupLayout(self) -> None:
        """设置布局"""
        # 创建总布局
        layout = QHBoxLayout()
        # 创建子布局
        vBoxLayout1 = QVBoxLayout()
        vBoxLayout2 = QVBoxLayout()
        hBoxLayout1 = QHBoxLayout()

        # 标签

        # 添加左侧头像
        vBoxLayout1.addWidget(self.iconLabel)

        # 添加右侧信息
        vBoxLayout2.addWidget(self.remarkLabel)
        vBoxLayout2.addWidget(self.userLabel)
        vBoxLayout2.addLayout(hBoxLayout1)
        vBoxLayout2.addSpacing(80)
        vBoxLayout2.addWidget(self.timeLabel)

        # 添加到总布局
        layout.addLayout(vBoxLayout1)
        layout.addSpacing(8)
        layout.addLayout(vBoxLayout2)

        # 设置布局
        layout.setContentsMargins(0, 0, 0, 0)
        vBoxLayout2.setContentsMargins(0, 8, 0, 5)

        self.setLayout(layout)

    def __showUserTrough(self) -> None:
        """显示用户名的槽函数"""
        if self.userLabel.text() == "*" * 30:
            self.userLabel.setText(
                self.user + "(None)" if self.steamId is None else f"({self.steamId})"
            )
            self.showUserAction.setText(self.tr("Hide User Name"))
        else:
            self.userLabel.setText("*" * 30)
            self.showUserAction.setText(self.tr("Show User Name"))


class AccountListView(SmoothScrollArea):
    """处理账号信息列表中的卡片展示"""

    def __init__(self, parent=None) -> None:
        """初始化"""
        super().__init__(parent=parent)
        self.view = QWidget(self)  # 创建一个QWidget实例作为视图
        self.vBoxLayout = QVBoxLayout(self.view)  # 为视图设立水平布局

        # 设置窗体小部件和调整大小属性
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        # 关闭垂直和水平滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 为视图设定名称
        self.view.setObjectName("view")

        # 使用样式表
        LoginPageStyleSheet.ACCOUNT_LIST_VIEW.apply(self)

    def __setupLayouts(self) -> None:
        """私有方法，用于设置布局属性"""
        # 设置内容边距
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        # 设置间隔
        self.vBoxLayout.setSpacing(0)
        # 设置对齐方式
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def addCard(self, account: dict):
        """添加卡片"""
        # 创建卡片
        card = AccountCard(account)
        # 添加到布局
        self.vBoxLayout.addWidget(card, Qt.AlignTop)
