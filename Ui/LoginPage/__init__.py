#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-7-19 下午 05:51
# @Author :Qiao
import sys
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from creart import add_creator, exists_module, create
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.LoginPage.Card import AddAccountCard, AccountListCard


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("LoginPage")

    def initialize(self, parent):
        """初始化"""
        self.parentClass = parent
        self.setupLayout()

    def setupLayout(self):
        """设置控件"""
        create(AddAccountCard).initialize(self.parentClass)

        layout = QGridLayout()
        layout.addWidget(create(AddAccountCard), 0, 0, 1, 1)
        layout.addWidget(create(AccountListCard), 0, 1, 1, 1)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)


class LoginPageClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LoginPage", "LoginPage"),)

    # 静态方法available()，用于检查模块"LoginPage"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginPage.Card.LoginPage")

    # 静态方法create()，用于创建LoginPage类的实例，返回值为LoginPage对象。
    @staticmethod
    def create(create_type: [LoginPage]) -> LoginPage:
        return LoginPage()


add_creator(LoginPageClassCreator)

if __name__ == "__main__":
    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    app.exec()
