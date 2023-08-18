#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :Icon.py
# @Time :2023-7-20 上午 11:47
# @Author :Qiao
from enum import Enum

from qfluentwidgets.common import getIconColor, Theme, FluentIconBase


class MainWindowIcon(FluentIconBase, Enum):
    LOGO = "Logo"

    def path(self, theme=Theme.AUTO) -> str:
        return f":MainWindow/image/MainWindow/{self.value}_{getIconColor(theme)}.svg"


class LoginPageIcon(FluentIconBase, Enum):
    STEAM = "Steam"

    def path(self, theme=Theme.AUTO) -> str:
        return f":LoginPage/image/LoginPage/{self.value}_{getIconColor(theme)}.svg"
