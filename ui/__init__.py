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
from PyQt5.Qt import *
from core import FileOperation
from ui.left_widget import top_icon_setup, left_button_setup, left_label_setup
from ui.login_widget import login_widget_setup


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
        self.setWindowTitle("Steam上号器 - 开发版 - Qiao")  # 设定窗口名
        self.setWindowIcon(QIcon("./img/icon/icon.ico"))  # 设定窗体图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体

    def read_qss_file(self) -> None:
        """读取QSS文件

        :return: None
        """
        with open('./QSS/ui.qss', 'r', encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    def setup_font(self) -> None:
        """窗体字体获取

        :return: None
        """
        self.font_name = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(r"./font/仓耳与墨W03.ttf"))[0]

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
        layout.addWidget(self.left_widget_setup(), 0, 0, 1, 1)
        layout.addWidget(self.page_widget_setup(), 0, 1, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
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
        layout.addWidget(left_button_setup(QFont(self.font_name, 13)), 2, 0, 1, 1, Qt.AlignTop)
        layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0, 1, 1)
        layout.addWidget(left_label_setup(self.font_name, self), 4, 0, 1, 1, Qt.AlignBottom)

        return widget

    def page_widget_setup(self) -> QStackedWidget:
        """页面窗体设置"""
        widget = QStackedWidget()
        widget.setObjectName("page_widget")

        # 接收控件和线程列队
        login_widget, self.pings = login_widget_setup(self.font_name, self)

        widget.addWidget(login_widget)

        widget.resize(500, 400)

        return widget

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
        if Qt.LeftButton and self._mouse_flag:
            # 如果是左键按下且鼠标跟踪打卡
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
        # 等待动画结束
        animation.finished.connect(lambda: self.close())
        # 启动动画
        animation.start()

        # 结束所有ping线程并实现关闭动画
        for ping in self.pings:
            # 结束ping线程
            ping.end_signal = False
        for ping in self.pings:
            # 等待线程安全退出
            ping.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SteamLoginUI()
    win.show()
    sys.exit(app.exec())
