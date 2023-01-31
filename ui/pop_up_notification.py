#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 19:20
# @Author  : 桥话语权
# @File    : pop_up_notification.py
# @Software: PyCharm
"""
 * 包含程序内用得上的一些弹窗
"""
import sys
from PyQt5.Qt import *


class ErrorPopUp(QWidget):
    """错误信息弹窗"""

    def __init__(self, title: str, txt: str, *args, **kwargs):
        """
        初始化窗体,导入参数
        :param title: str
        :param txt: str
        :param args: any
        :param kwargs: any
        """
        super(ErrorPopUp, self).__init__()
        self.title = title
        self.text = txt
        self.setup_window()
        self.setup_form()

    def setup_window(self):
        """
        设定窗体参数
        :return:
        """
        self.setFixedSize(300, 260)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体

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

        # 添加阴影
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 0)  # 偏移
        effect_shadow.setBlurRadius(10)  # 阴影半径
        effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(effect_shadow)  # 将设置套用到widget窗口中

        # 显示窗体
        self.setLayout(self.base_layout)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ErrorPopUp("1", "2")
    win.show()
    sys.exit(app.exec())
