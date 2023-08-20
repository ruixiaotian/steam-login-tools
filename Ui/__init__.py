#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-7-19 下午 05:50
# @Author :Qiao
import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QApplication
from creart import create
from qfluentwidgets.common import (
    isDarkTheme,
    setTheme,
    Theme,
    setThemeColor,
    FluentIcon,
)
from qfluentwidgets.components import (
    NavigationItemPosition,
    MessageBox,
)
from qfluentwidgets.window import MSFluentWindow

from Ui.Icon import MainWindowIcon
from Ui.LoginPage import LoginPage
from Ui.HomePage import HomeWidget
from Ui.SetupPage import SetupWidget
from Ui.resource import resource


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.setupItem()

    def setupWindow(self):
        # 设置标题栏
        self.setWindowTitle("Steam Login Tools")
        self.setWindowIcon(QIcon(MainWindowIcon.LOGO.path()))
        # 设置大小
        self.setMinimumSize(1080, 780)
        # 设置窗体打开时居中
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def setupItem(self):
        """设置侧边栏"""

        # 初始化子页面
        create(HomeWidget).initialize(self)
        create(LoginPage).initialize(self)
        create(SetupWidget).initialize(self)

        # 添加子页面
        self.addSubInterface(
            interface=create(HomeWidget),
            icon=FluentIcon.HOME,
            text=self.tr("Home"),
            position=NavigationItemPosition.TOP,
        )
        self.addSubInterface(
            interface=create(LoginPage),
            icon=FluentIcon.ADD,
            text=self.tr("Add"),
            position=NavigationItemPosition.TOP,
        )

        # 添加设置
        self.addSubInterface(
            interface=create(SetupWidget),
            icon=FluentIcon.SETTING,
            text=self.tr("Setup"),
            position=NavigationItemPosition.BOTTOM,
        )

        # 添加赞助
        self.navigationInterface.addItem(
            routeKey="sponsor",
            icon=FluentIcon.EXPRESSIVE_INPUT_ENTRY,
            text="Sponsor",
            onClick=self.showSponsorship,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

    def showSponsorship(self):
        title = "Sponsorship"
        content = self.tr(
            "It's not easy to develop programs individually. If this project has been helpful to you, "
            "you might consider treating the author to a cup of milk tea 🍵. "
            "Your support is the biggest motivation for me to maintain the project."
        )
        box = MessageBox(title, content, self)
        box.yesButton.setText(self.tr("Coming!"))
        box.cancelButton.setText(self.tr("Next time, definitely"))
        if box.exec():
            QDesktopServices.openUrl(
                QUrl(r"https://github.com/ruixiaotian/steam-login-tools")
            )

    @staticmethod
    def switchThemes():
        if isDarkTheme():
            setTheme(Theme.LIGHT)
            setThemeColor(QColor("#43CCF8"))
        else:
            setTheme(Theme.DARK)
            setThemeColor(QColor("#19DEEF"))


if __name__ == "__main__":
    #  适配高DPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
