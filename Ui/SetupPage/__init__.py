#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-8-18 下午 06:34
# @Author :Qiao
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel
from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from qfluentwidgets.common import FluentIcon, setTheme, setThemeColor
from qfluentwidgets.components import (
    InfoBar,
    ScrollArea,
    ExpandLayout,
    SettingCardGroup,
    OptionsSettingCard,
    CustomColorSettingCard,
    ComboBoxSettingCard,
)

from Core.config import cfg
from Ui.StyleSheet import SetupPageStyleSheet


class SetupWidget(ScrollArea):
    """设置页面"""

    def __init__(self, parent=None):
        """初始化"""
        super().__init__(parent=parent)

    def initialize(self, parent):
        """初始化"""
        self.parentClass = parent
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        # 页面标签
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # 设置属性
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")

        # 引用样式表
        self.scrollWidget.setObjectName("scrollWidget")
        self.settingLabel.setObjectName("settingLabel")
        SetupPageStyleSheet.SETTING_PAGE.apply(self)

        # 初始化控件等
        self.personalSetup()
        # 设置布局
        self.__setupLayout()
        # 链接信号
        self.__connectSignal()

    def personalSetup(self):
        """个性化 - 设置项"""

        # 创建设置组
        self.personalGroup = SettingCardGroup(
            title=self.tr("Personalize"), parent=self.scrollWidget
        )
        # 创建设置项
        self.themeCard = OptionsSettingCard(
            configItem=cfg.themeMode,
            icon=FluentIcon.BRUSH,
            title=self.tr("Switch themes"),
            content=self.tr("Switch the theme of the app"),
            texts=[
                self.tr("Light"),
                self.tr("Dark"),
                self.tr("Use system setting"),
            ],
            parent=self.personalGroup,
        )
        self.themeColorCard = CustomColorSettingCard(
            configItem=cfg.themeColor,
            icon=FluentIcon.PALETTE,
            title=self.tr("Theme color"),
            content=self.tr("Choose a theme color"),
            parent=self.personalGroup,
        )
        self.languageCard = ComboBoxSettingCard(
            configItem=cfg.language,
            icon=FluentIcon.LANGUAGE,
            title=self.tr("Language"),
            content=self.tr("Set your preferred language for UI"),
            texts=["简体中文", "繁体中文", "English", self.tr("Use system setting")],
            parent=self.personalGroup,
        )

    def __setupLayout(self):
        """布局设置"""
        self.settingLabel.move(36, 30)

        # 添加卡片到组
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.languageCard)

        # 添加组到布局
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.personalGroup)

    def __connectSignal(self):
        """链接信号"""
        # config提供的信号
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # 个性化
        cfg.themeChanged.connect(setTheme)
        self.themeColorCard.colorChanged.connect(setThemeColor)

    def __showRestartTooltip(self):
        """显示重启提示"""
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )


class SetupWidgetClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SetupPage", "SetupWidget"),)

    # 静态方法available()，用于检查模块"SetupWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SetupPage")

    # 静态方法create()，用于创建SetupWidget类的实例，返回值为SetupWidget对象。
    @staticmethod
    def create(create_type: [SetupWidget]) -> SetupWidget:
        return SetupWidget()


add_creator(SetupWidgetClassCreator)
