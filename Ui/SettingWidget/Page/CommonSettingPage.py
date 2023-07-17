#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CommonSettingPage.py
# @Time :2023-7-17 下午 04:08
# @Author :Qiao
from abc import ABC

from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.SettingWidget.Page.Base import SettingWidgetBase, CardBase


class CommonSettingPage(SettingWidgetBase):
    def __init__(self):
        super().__init__()

    def initialize(self, parent, font: str, page):
        """初始化"""
        self.font = font
        self.parent = parent
        self.page = page
        self.title_content = "通用设置"
        self.setupContent()
        self.setupLayout()

    def setupContent(self):
        """设置内容"""
        initiate_setting_card = InitiateSettingCard(self.font)
        self.scroll_content.append(initiate_setting_card)


class InitiateSettingCard(CardBase):
    def __init__(self, font: str):
        super().__init__()
        self.title_content = "启动设置"
        self.card_height = 185
        self.font = font
        self.setupLayout()


class CommonSettingPageClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Ui.SettingWidget.Page.CommonSettingPage", "CommonSettingPage"
        ),
    )

    # 静态方法available()，用于检查模块"Ui.SettingWidget.Page.CommonSettingPage"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Page.CommonSettingPage")

    # 静态方法create()，用于创建CommonSettingPage类的实例，返回值为CommonSettingPage对象。
    @staticmethod
    def create(create_type: [CommonSettingPage]) -> CommonSettingPage:
        return CommonSettingPage()


add_creator(CommonSettingPageClassCreator)
