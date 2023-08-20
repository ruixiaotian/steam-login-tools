#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :StyleSheet.py
# @Time :2023-7-20 下午 09:13
# @Author :Qiao
from pathlib import Path
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class HomePageStyleSheet(StyleSheetBase, Enum):
    """主页样式表"""
    HOME_WIDGET = "home_widget"
    LINK_CARD = "link_card"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return Path(f":HomePage/qss/{theme.value.lower()}/{self.value}.qss").__str__()


class LoginPageStyleSheet(StyleSheetBase, Enum):
    """登录页面样式表"""

    LOGIN_PAGE = "login_page"
    ACCOUNT_LIST_VIEW = "account_card"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return Path(f":LoginPage/qss/{theme.value.lower()}/{self.value}.qss").__str__()


class SetupPageStyleSheet(StyleSheetBase, Enum):
    """设置页面样式表"""

    SETTING_PAGE = "setup_page"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return Path(f":SetupPage/qss/{theme.value.lower()}/{self.value}.qss").__str__()
