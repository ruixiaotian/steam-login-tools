#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :AuthorizationSettingPage.py
# @Time :2023-7-17 下午 05:28
# @Author :Qiao
from abc import ABC

from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.SettingWidget.Page.Base import SettingWidgetBase


class AuthorizationSettingPage(SettingWidgetBase):
    def __init__(self):
        super().__init__()

    def initialize(self, parent, font: str, page):
        """初始化"""
        self.font = font
        self.parent = parent
        self.page = page
        self.title_content = "授权设置"
        self.setupLayout()


class AuthorizationSettingPageClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Ui.SettingWidget.Page.AuthorizationSettingPage", "AuthorizationSettingPage"
        ),
    )

    # 静态方法available()，用于检查模块"Ui.SettingWidget.Page.AuthorizationSettingPage"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Page.AuthorizationSettingPage")

    # 静态方法create()，用于创建AuthorizationSettingPage类的实例，返回值为AuthorizationSettingPage对象。
    @staticmethod
    def create(create_type: [AuthorizationSettingPage]) -> AuthorizationSettingPage:
        return AuthorizationSettingPage()


add_creator(AuthorizationSettingPageClassCreator)