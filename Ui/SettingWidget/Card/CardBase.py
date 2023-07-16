#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :CardBase.py
# @Time :2023-7-11 上午 11:29
# @Author :Qiao
from pathlib import Path

from PyQt5.QtCore import QEvent, Qt, QEasingCurve, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QMouseEvent, QFont
from PyQt5.QtWidgets import (
    QGraphicsOpacityEffect,
    QGridLayout,
    QLabel,
    QWidget,
    QMainWindow,
)
from creart import create

from Core.EventAnimation.AnimationObject import Animation
from Core.FileOperation import FileOperation


class CardBase(QMainWindow):
    """卡片的基类"""

    icon_label: QLabel | None
    text_label: QLabel | None
    icon_path: Path | str
    text_content: str
    mouse_state: bool
    animation_status: bool

    # 自定义信号
    clicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.icon_label = QLabel()
        self.text_label = QLabel()
        self.mouse_state = False
        self.animation_status = False

    def baseInitialize(self):
        self.setupForm()
        self.setupLayout()
        self.setup_qss()

    def setup_qss(self) -> None:
        """读取QSS文件"""
        self.setStyleSheet(create(FileOperation).qss_content)

    def setupForm(self) -> None:
        """窗体设定"""
        # 透明窗体
        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setObjectName("base_widget")  # 设置对象名称
        self.base_layout = QGridLayout()  # 创建透明窗口布局
        self.base_widget.setLayout(self.base_layout)  # 设置布局
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏背景

        # 主窗体
        self.main_widget = QWidget()  # 创建主窗体
        self.main_widget.setFixedSize(120, 120)
        self.main_widget.setObjectName("SettingPageBaseCard")  # 设置主窗体对象名称
        self.base_layout.addWidget(self.main_widget)  # 添加到布局

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

    def setupLayout(self) -> None:
        """设定窗体内布局"""
        layout = QGridLayout()  # 创建网格布局
        layout.addWidget(self.__setIcon(), 0, 0, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.__setText(), 1, 0, 1, 1, Qt.AlignCenter)
        layout.setContentsMargins(0, 30, 0, 10)
        self.main_widget.setLayout(layout)  # 设置窗体内布局

    def __setIcon(self) -> QLabel:
        """图标设置"""
        # 创建子控件
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(self.icon_path.__str__()))
        self.icon_label.setObjectName("card_icon_label")
        self.icon_label.setScaledContents(True)  # 设置自适应
        self.icon_label.setFixedSize(64, 64)

        return self.icon_label

    def __setText(self) -> QLabel:
        """文字设置"""
        # 创建子控件
        self.text_label = QLabel(self.text_content)
        self.text_label.setObjectName("card_test_label")
        self.text_label.setFont(QFont(self.font, 10))

        # 实现透明
        self.text_label_opacity = QGraphicsOpacityEffect()
        self.text_label_opacity.setOpacity(0)
        self.text_label.setGraphicsEffect(self.text_label_opacity)

        return self.text_label

    def __iconUp(self) -> None:
        """图标缩小并且向上移动"""
        # 设置动画状态
        self.animation_status = True
        # 创建移动动画
        animation_obj = Animation(self.icon_label)
        move_animation = animation_obj.setPos(
            time=300,
            easing_curve=QEasingCurve.OutBack,
            start_value=QPoint(self.icon_label.x(), self.icon_label.y()),
            end_value=QPoint(self.icon_label.x(), self.icon_label.y() - 5),
        )
        # 添加到串行动画组
        animation_group = animation_obj.addAnimationGroup(
            [move_animation], parallel_mod=True
        )
        # 输入账密控件,和状态信息控件隐藏
        animation_group.finished.connect(
            lambda: (
                (self.__test_show(), self.__setupAnimationState(False))
                if self.mouse_state
                else self.__iconDown()
            )
        )
        # 启动动画
        animation_group.start()

    def __iconDown(self) -> None:
        """图标缩小并且向上移动"""
        # 设置动画状态
        self.animation_status = True
        # 创建移动动画
        animation_obj = Animation(self.icon_label)
        move_animation = animation_obj.setPos(
            time=300,
            easing_curve=QEasingCurve.OutBack,
            start_value=QPoint(self.icon_label.x(), self.icon_label.y()),
            end_value=QPoint(self.icon_label.x(), self.icon_label.y() + 5),
        )
        # 添加到串行动画组
        animation_group = animation_obj.addAnimationGroup(
            [move_animation], parallel_mod=True
        )
        # 输入账密控件,和状态信息控件隐藏
        animation_group.finished.connect(
            lambda: (
                (self.__test_hide(), self.__setupAnimationState(False))
                if not self.mouse_state
                else self.__iconUp()
            )
        )
        # 启动动画
        animation_group.start()

    def __test_show(self) -> None:
        """显示label"""
        self.__num = 1

        def timeout():
            """超时函数：改变透明度"""
            self.text_label_opacity.setOpacity(self.__num / 100)
            self.text_label.setGraphicsEffect(self.text_label_opacity)  # 改变标签透明度
            self.__num += 20
            if self.__num >= 100:
                self.text_label_opacity.setOpacity(1)
                self.timer.stop()  # 计时器停止
                self.timer.deleteLater()

        self.timer = QTimer()  # 计时器
        self.timer.setInterval(5)  # 设置间隔时间，毫秒为单位
        self.timer.timeout.connect(timeout)  # 超时槽函数，每到达间隔时间，调用该函数
        self.timer.start()  # 计时器开始

    def __test_hide(self) -> None:
        """显示label"""
        self.__num = 100

        def timeout():
            """超时函数：改变透明度"""
            self.text_label_opacity.setOpacity(self.__num / 100)
            self.text_label.setGraphicsEffect(self.text_label_opacity)  # 改变标签透明度
            self.__num -= 20
            if self.__num <= 0:
                self.text_label_opacity.setOpacity(0)
                self.timer.stop()  # 计时器停止
                self.timer.deleteLater()

        self.timer = QTimer()  # 计时器
        self.timer.setInterval(5)  # 设置间隔时间，毫秒为单位
        self.timer.timeout.connect(timeout)  # 超时槽函数，每到达间隔时间，调用该函数
        self.timer.start()  # 计时器开始

    def __setupAnimationState(self, state: bool) -> None:
        if state:
            self.animation_status = True
        else:
            self.animation_status = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """重写鼠标按下事件进行监听"""
        self.clicked.emit()

    def enterEvent(self, event: QEvent) -> None:
        """重写鼠标移入实现进行监听"""
        self.mouse_state = True
        if not self.animation_status:
            self.__iconUp()

    def leaveEvent(self, event: QEvent) -> None:
        """重写鼠标移出事件进行监听"""
        self.mouse_state = False
        if not self.animation_status:
            self.__iconDown()
