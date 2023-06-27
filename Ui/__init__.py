#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 0:41
# @Author  : 桥话语权
# @File    : __init__.py.py
# @Software: PyCharm
"""
* 程序UI
"""

import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFontDatabase, QMouseEvent, QCloseEvent, QColor, QFont
from PyQt5.QtWidgets import QWidget, QMainWindow, QStackedWidget, QApplication, QSizePolicy, QGridLayout, \
    QGraphicsDropShadowEffect, QSpacerItem
from creart import create
from loguru import logger

from Ui.LeftWidget import top_icon_setup, left_button_setup, left_label_setup
from Ui.LoginWidget import LoginWidget
from Ui.NetWidget import NetWidget
from Ui.OtherWidget import SteamSettingWidget, FixLoginWidget, BulkImportWidget
from Ui.SettingWidget import SettingWidget


class SteamLoginUI(QMainWindow):
    """程序UI的绘制"""
    close_state = True

    def __init__(self) -> None:
        """初始化程序设定"""
        super(SteamLoginUI, self).__init__()
        self.setup_window()
        self.setup_font()
        self.setup_form()
        self.setup_layout()
        self.read_qss_file()

    def setup_window(self) -> None:
        """设定窗体各类参数

        :return: None
        """
        self.setFixedSize(750, 500)  # 设定窗体大小
        self.setWindowTitle("Steam上号器 - 测试版 - Qiao")  # 设定窗口名
        self.setWindowIcon(QIcon("./img/icon/icon.ico"))  # 设定窗体图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体

    def read_qss_file(self) -> None:
        """读取QSS文件

        :return: None
        """
        qss_path = Path("./QSS/UiQss")
        qss_content = "".join([f.read_text(encoding="utf-8") for f in qss_path.rglob("*") if f.is_file()])
        self.setStyleSheet(qss_content)

    def setup_font(self) -> None:
        """窗体字体获取

        :return: None
        """
        self.font_name = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(r"./font/W03.ttf"))[0]

    def setup_form(self) -> None:
        """窗体设定

        :return: None
        """
        # 透明窗体
        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setObjectName("base_widget")  # 设置对象名称
        self.base_layout = QGridLayout()  # 创建透明窗口布局
        self.base_widget.setLayout(self.base_layout)  # 设置布局
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏背景

        # 主窗体
        self.main_widget = QWidget()  # 创建主窗体
        self.main_widget.setObjectName("main_widget")  # 设置主窗体对象名称
        self.base_layout.addWidget(self.main_widget)  # 添加到布局

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 添加阴影
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 1)  # 偏移
        effect_shadow.setBlurRadius(12)  # 阴影半径
        effect_shadow.setColor(QColor("#1DBEF5"))  # 阴影颜色
        self.main_widget.setGraphicsEffect(effect_shadow)  # 将设置套用到widget窗口中

    def setup_layout(self) -> None:
        """设定窗体内布局"""
        layout = QGridLayout()  # 创建网格布局
        layout.addWidget(self.page_widget_setup(), 0, 1, 1, 1)
        layout.addWidget(self.left_widget_setup(), 0, 0, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(0)  # 移除间隙
        self.main_widget.setLayout(layout)  # 设置窗体内布局

    def left_widget_setup(self) -> QWidget:
        """左方窗体设置"""
        widget = QWidget()
        layout = QGridLayout(widget)
        # 窗体设置
        widget.resize(160, 490)
        widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        widget.setObjectName("left_widget")

        # 添加到布局中
        layout.addWidget(top_icon_setup(QFont(self.font_name, 12)), 0, 0, 1, 1, Qt.AlignTop)
        layout.addItem(QSpacerItem(10, 50, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 0, 1, 1)
        layout.addWidget(left_button_setup(QFont(self.font_name, 13), self.page_widget), 2, 0, 1, 1, Qt.AlignTop)
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0, 1, 1)
        layout.addWidget(left_label_setup(self.font_name, self), 4, 0, 1, 1, Qt.AlignBottom)

        return widget

    def page_widget_setup(self) -> QStackedWidget:
        """页面窗体设置"""
        self.page_widget = QStackedWidget()

        """页面设置"""
        # 登录页面
        create(LoginWidget).initialize(self, self.font_name)
        login_widget = create(LoginWidget).login_widget_setup(self)
        self.pings = create(LoginWidget).pings

        # 网络加速页面
        net = NetWidget(self, self.font_name)
        net_widget = net.net_widget_setup()

        # 设置页面
        setting = SettingWidget(self, self.font_name)
        setting_widget = setting.setting_widget_setup()

        # 修复登录页面
        fix_wgt = create(FixLoginWidget)
        fix_wgt.initialize(self, self.font_name, self.page_widget)
        fix_widget = fix_wgt.fix_widget_setup()

        # 批量导入页面
        bulk_wgt = create(BulkImportWidget)
        bulk_wgt.initialize(self, self.font_name, self.page_widget)
        bulk_widget = bulk_wgt.bulk_import_widget_setup()

        # Steam设置页面
        set_wgt = create(SteamSettingWidget)
        set_wgt.initialize(self, self.font_name, self.page_widget)
        dw_widget = set_wgt.dw_widget_setup()

        wgt_list = [
            login_widget, net_widget, setting_widget,
            fix_widget, bulk_widget, dw_widget
        ]
        for i in wgt_list:
            # 循环加入QStackedWidget
            self.page_widget.addWidget(i)

        self.page_widget.resize(500, 400)

        return self.page_widget

    def thread_exits(self):
        """退出线程函数,让子线程安全的退出"""
        # 结束所有ping线程
        logger.info(f"准备退出子线程 - 当前退出：Ping")
        for ping in self.pings:
            # 结束ping线程
            ping.end_signal = False
            logger.info(f"正在结束ping线程 {ping}")
        for ping in self.pings:
            # 等待线程安全退出
            ping.quit()
            logger.info(f"{ping} 线程安全退出")

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """重构鼠标按下事件函数,进行鼠标跟踪以及获取相对位置

        :param event:
        :return: None
        """
        if event.button() == Qt.LeftButton:
            # 如果按下按钮为左键
            self._mouse_flag = True  # 设置鼠标跟踪开关为True
            self.m_pos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """重构鼠标移动事件函数,进行监控鼠标移动并且判断是否拖动窗口

        :param event:
        :return: None
        """
        if Qt.LeftButton and self._mouse_flag and self.close_state:
            # 如果是左键按下鼠标且跟踪打开, 不处于关闭状态,则可以拖动窗口
            self.move(event.globalPos() - self.m_pos)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """重构鼠标松开事件函数,进行监控鼠标状态

        :param event:
        :return: None
        """
        self._mouse_flag = False  # 设置鼠标跟踪为关

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.close_state:  # 判断是否关闭
            event.ignore()
            self.close_state = False
        # 创建动画对象
        animation = QPropertyAnimation(self, b"windowOpacity", self)
        # 设置透明度
        animation.setDuration(2000)
        animation.setStartValue(1)
        animation.setEndValue(0)

        # 退出线程
        self.thread_exits()

        animation.finished.connect(lambda: sys.exit(0))  # 调用sys防止子窗体未退出
        # 启动动画
        animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SteamLoginUI()
    win.show()
    sys.exit(app.exec())
