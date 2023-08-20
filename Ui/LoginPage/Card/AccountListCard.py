#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :ToolsCard.py
# @Time :2023-7-20 下午 09:52
# @Author :Qiao
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from creart import add_creator, exists_module, create
from creart.creator import AbstractCreator, CreateTargetInfo
from qfluentwidgets.common import FluentIcon
from qfluentwidgets.components import (
    CardWidget,
    IconWidget,
    BodyLabel,
)

from Core.FileFunction import JsonFunc
from Ui.LoginPage.Card.AccountListItem import AccountListView
from Ui.StyleSheet import LoginPageStyleSheet


class AccountListCard(CardWidget):
    def __init__(self):
        super().__init__()
        self.createControl()
        self.setupControl()
        self.addCard()
        self.setupLayout()
        LoginPageStyleSheet.LOGIN_PAGE.apply(self)

    def createControl(self):
        """创建控件"""
        self.icon = IconWidget()
        self.title = BodyLabel()
        self.accountCardView = AccountListView()

    def setupControl(self):
        """设置控件属性"""
        # 设置text
        self.title.setText(self.tr("Account List"))

        # 设置Icon
        self.icon.setIcon(FluentIcon.TAG)
        self.icon.setMinimumSize(16, 16)
        self.icon.setMaximumSize(20, 20)

        # 设置对象名称
        self.title.setObjectName("AccountListCard-title")

        # 设置宽高
        self.title.setMaximumHeight(22)
        self.icon.setMaximumHeight(20)

    def addCard(self):
        """添加卡片"""
        for cammy in create(JsonFunc).readJson(create(JsonFunc).cammy_path):
            self.accountCardView.addCard(cammy)

    def setupLayout(self):
        """设置布局"""
        # 水平布局
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.icon)
        hLayout1.addWidget(self.title)
        hLayout1.addItem(QSpacerItem(30, 1, hPolicy=QSizePolicy.Maximum))

        # 网格布局
        layout = QGridLayout()
        layout.addLayout(hLayout1, 0, 0, 1, 2, Qt.AlignTop)
        layout.addWidget(self.accountCardView, 1, 0, 1, 2)

        # 设置布局
        hLayout1.setSpacing(10)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setVerticalSpacing(8)

        self.setLayout(layout)


class AccountListCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo("Ui.LoginPage.Card.AccountListCard", "AccountListCard"),
    )

    # 静态方法available()，用于检查模块"AccountListCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginPage.Card.AccountListCard")

    # 静态方法create()，用于创建AccountListCard类的实例，返回值为AccountListCard对象。
    @staticmethod
    def create(create_type: [AccountListCard]) -> AccountListCard:
        return AccountListCard()


add_creator(AccountListCardClassCreator)
