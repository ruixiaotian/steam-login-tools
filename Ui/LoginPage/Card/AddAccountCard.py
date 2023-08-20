#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :AddAccount.py
# @Time :2023-7-20 上午 10:58
# @Author :Qiao
from abc import ABC
from copy import deepcopy
from json.decoder import JSONDecodeError

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
    LineEdit,
    PushButton,
    PrimaryPushButton,
    IconWidget,
    BodyLabel,
    ToolTipFilter,
    ToolTipPosition,
    InfoBar,
    InfoBarPosition,
)

from Core.FileFunction import Template, JsonFunc
from Core.share.ErrorHandling import JsonDecodingErrorDispose
from Ui.Icon import LoginPageIcon
from Ui.StyleSheet import LoginPageStyleSheet


class AddAccountCard(CardWidget):
    def __init__(self):
        super().__init__()
        LoginPageStyleSheet.LOGIN_PAGE.apply(self)

    def initialize(self, parent):
        """初始化"""
        self.parentClass = parent

        self.__createControl()
        self.__setupControl()
        self.__connectSignal()
        self.__setupLayout()

    def __setupLayout(self):
        """设置布局"""
        # 水平布局
        h_layout_1 = QHBoxLayout()
        h_layout_1.addWidget(self.icon)
        h_layout_1.addWidget(self.title)
        h_layout_1.addItem(QSpacerItem(30, 1, hPolicy=QSizePolicy.Maximum))

        h_layout_2 = QHBoxLayout()
        h_layout_2.addItem(QSpacerItem(30, 1, hPolicy=QSizePolicy.Expanding))
        h_layout_2.addWidget(self.steam_logo)
        h_layout_2.addItem(QSpacerItem(30, 1, hPolicy=QSizePolicy.Expanding))

        # 网格布局
        layout = QGridLayout()
        layout.addLayout(h_layout_1, 0, 0, 1, 2, Qt.AlignTop)
        layout.addLayout(h_layout_2, 2, 0, 1, 2)
        layout.addWidget(self.user_edit, 4, 0, 1, 2)
        layout.addWidget(self.password_edit, 5, 0, 1, 2)
        layout.addWidget(self.ssfn_edit, 6, 0, 1, 2)
        layout.addWidget(self.login_button, 7, 0, 1, 1)
        layout.addWidget(self.save_button, 7, 1, 1, 1)
        layout.addItem(QSpacerItem(10, 100, vPolicy=QSizePolicy.Expanding), 1, 0, 1, 2)
        layout.addItem(QSpacerItem(10, 100, vPolicy=QSizePolicy.Expanding), 3, 0, 1, 2)

        # 设置布局
        h_layout_1.setSpacing(10)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setVerticalSpacing(15)

        self.setLayout(layout)

    def __createControl(self):
        """创建控件"""
        self.icon = IconWidget()
        self.title = BodyLabel()
        self.steam_logo = IconWidget()
        self.user_edit = LineEdit()
        self.password_edit = LineEdit()
        self.ssfn_edit = LineEdit()
        self.login_button = PushButton()
        self.save_button = PrimaryPushButton()

        self.tips_list = [
            self.user_edit,
            self.password_edit,
            self.ssfn_edit,
            self.login_button,
            self.save_button,
        ]

    def __setupControl(self):
        """设置控件属性"""

        # 设置text
        self.title.setText(self.tr("Add Account"))
        self.user_edit.setPlaceholderText(self.tr("USER-UserName"))
        self.password_edit.setPlaceholderText(self.tr("PWD-PassWord"))
        self.ssfn_edit.setPlaceholderText(self.tr("SSFN-SentryFile"))
        self.login_button.setText(self.tr("Login"))
        self.save_button.setText(self.tr("Save"))

        # 设置Icon
        self.icon.setIcon(FluentIcon.ADD_TO)
        self.icon.setMinimumSize(16, 16)
        self.icon.setMaximumSize(20, 20)
        self.steam_logo.setIcon(LoginPageIcon.STEAM)
        self.steam_logo.setMinimumSize(128, 128)
        self.steam_logo.setMaximumSize(512, 512)

        # 设置Tip
        self.user_edit.setToolTip(self.tr("Enter your account number here"))
        self.password_edit.setToolTip(self.tr("Enter your account password here"))
        self.ssfn_edit.setToolTip(self.tr("Enter your account ssfn here"))
        self.login_button.setToolTip(self.tr("Log in to your account"))
        self.save_button.setToolTip(self.tr("Save the data in the input box above"))

        for tips in self.tips_list:
            # 循环添加tips
            tips.installEventFilter(ToolTipFilter(tips, 300, ToolTipPosition.TOP))

        # 设置对象名称
        self.title.setObjectName("AddAccountCard-title")

        # 设置宽高
        self.title.setMaximumHeight(22)
        self.icon.setMaximumHeight(20)
        self.setMaximumWidth(400)

    def __connectSignal(self):
        """连接信号"""
        self.login_button.clicked.connect(self.__loginButtonTrough)
        self.save_button.clicked.connect(self.__saveButtonTrough)

    def __loginButtonTrough(self):
        """登录按钮的槽函数"""
        if not self.user_edit.text() or not self.password_edit.text():
            # 如果用户未输入账号或者密码就弹出提示框
            self.__editTips()
            return
        if self.ssfn_edit.text() and self.ssfn_edit.text().startswith("ssfn"):
            # 如果输入了ssfn 且 格式正确
            self.__ssfnTips(True)
        else:
            # 没有输入或者不正确
            self.__ssfnTips(False)

    def __saveButtonTrough(self):
        """保存按钮槽函数"""
        # 拷贝一个数据模板
        cammy_item = deepcopy(Template.cammy_item_template)
        if not self.user_edit.text() or not self.password_edit.text():
            # 如果用户未输入账号或者密码就弹出提示框
            self.__editTips()
            return
        # 添加数据
        cammy_item["User"] = self.user_edit.text()
        cammy_item["PassWord"] = self.user_edit.text()
        try:
            # 读取数据文件并添加
            cammyData: list = create(JsonFunc).readJson(create(JsonFunc).cammy_path)
            cammyData.append(cammy_item)
            # 写入数据文件
            create(JsonFunc).writeJson(create(JsonFunc).cammy_path, cammyData)
            # 提示框判断
            if self.ssfn_edit.text() and self.ssfn_edit.text().startswith("ssfn"):
                # 如果输入了ssfn 且 格式正确
                self.__ssfnTips(True)
                cammy_item["SSFN"] = self.user_edit.text()
            else:
                # 没有输入或者不正确
                self.__ssfnTips(False)
        except JSONDecodeError:
            # 如果写入Json时发生错误
            JsonDecodingErrorDispose(
                create(JsonFunc).cammy_path, self, self.parentClass
            )

    def __editTips(self):
        """用户名或密码未输入提示"""
        InfoBar.warning(
            title=self.tr("Incomplete parameters"),
            content=self.tr(
                "The account and password must be entered,\n"
                "please check if they are complete"
            ),
            orient=Qt.Vertical,
            isClosable=False,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=3000,
            parent=self.parentClass,
        )

    def __ssfnTips(self, isItCorrect: bool):
        """SSFN提示"""
        if isItCorrect:
            InfoBar.info(
                title=self.tr("Tip"),
                content=self.tr(
                    "You have entered SSFN and the format is correct.\n"
                    "Skip mailbox verification will be enabled by default"
                ),
                orient=Qt.Vertical,
                isClosable=False,
                duration=2500,
                position=InfoBarPosition.TOP,
                parent=self.parentClass,
            )
        else:
            InfoBar.info(
                title=self.tr("Tip"),
                content=self.tr(
                    "You did not enter SSFN or the format is incorrect.\n"
                    "Skipping mailbox verification will be disabled by default"
                ),
                orient=Qt.Vertical,
                isClosable=False,
                duration=2500,
                position=InfoBarPosition.TOP,
                parent=self.parentClass,
            )


class AddAccountCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LoginPage.Card.AddAccountCard", "AddAccountCard"),)

    # 静态方法available()，用于检查模块"AddAccountCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginPage.Card.AddAccountCard")

    # 静态方法create()，用于创建AddAccountCard类的实例，返回值为AddAccountCard对象。
    @staticmethod
    def create(create_type: [AddAccountCard]) -> AddAccountCard:
        return AddAccountCard()


add_creator(AddAccountCardClassCreator)
