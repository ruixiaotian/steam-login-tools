#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/5 11:25
# @Author  : 桥话语权
# @File    : event_animation.py
# @Software: PyCharm
"""
 *            佛曰:
 *                   写字楼里写字间，写字间里程序员；
 *                   程序人员写程序，又拿程序换酒钱。
 *                   酒醒只在网上坐，酒醉还来网下眠；
 *                   酒醉酒醒日复日，网上网下年复年。
 *                   但愿老死电脑间，不愿鞠躬老板前；
 *                   奔驰宝马贵者趣，公交自行程序员。
 *                   别人笑我忒疯癫，我笑自己命太贱；
 *                   不见满街漂亮妹，哪个归得程序员？
"""
from PyQt5.Qt import *


def account_animation_max(
        info_widget: QWidget,
        account_widget: QWidget,
        status_widget: QWidget
):
    """
    将账号信息控件最大化，其他控件隐藏

    :param info_widget: 账号信息控件
    :param account_widget: 输入账密控件
    :param status_widget: 状态信息控件
    :return:
    """

    # 移动
    info_widget_animation_move = QPropertyAnimation(info_widget, b"pos")  # 创建移动动画对象
    info_widget_animation_move.setDuration(800)  # 设置动画持续时间
    info_widget_animation_move.setStartValue(QPoint(info_widget.x(), info_widget.y()))  # 初始位置
    info_widget_animation_move.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    info_widget_animation_move.setEndValue(
        QPoint(
            info_widget.x(),
            info_widget.y() - 206
        )
    )  # 结束位置

    # 放大
    info_widget_animation_resize = QPropertyAnimation(info_widget, b"size", info_widget)  # 创建放大动画对象
    info_widget_animation_resize.setDuration(600)  # 设置动画持续时间
    info_widget_animation_resize.setStartValue(QSize(info_widget.width(), info_widget.height()))  # 初始位置
    info_widget_animation_resize.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    info_widget_animation_resize.setEndValue(
        QSize(
            info_widget.width(),
            info_widget.height() + 206
        )
    )  # 结束位置

    # 添加到动画组
    # 串行动画组
    animation_sequent_group = QParallelAnimationGroup(info_widget)
    animation_sequent_group.addAnimation(info_widget_animation_move)
    animation_sequent_group.addAnimation(info_widget_animation_resize)

    # 输入账密控件,和状态信息控件隐藏
    animation_sequent_group.finished.connect(
        lambda: (account_widget.setHidden(True), status_widget.setHidden(True)))

    # 启动动画
    animation_sequent_group.start()


def account_animation_min(
        info_widget: QWidget,
        account_widget: QWidget,
        status_widget: QWidget
):
    """
    将账号信息控件最小化，其他控件显示

    :param info_widget:
    :param account_widget:
    :param status_widget:
    :return:
    """

 # 移动
    info_widget_animation_move = QPropertyAnimation(info_widget, b"pos")  # 创建移动动画对象
    info_widget_animation_move.setDuration(800)  # 设置动画持续时间
    info_widget_animation_move.setStartValue(QPoint(info_widget.x(), info_widget.y()))  # 初始位置
    info_widget_animation_move.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    info_widget_animation_move.setEndValue(
        QPoint(
            info_widget.x(),
            info_widget.y() + 206
        )
    )  # 结束位置

    # 缩小
    info_widget_animation_resize = QPropertyAnimation(info_widget, b"size", info_widget)  # 创建放大动画对象
    info_widget_animation_resize.setDuration(600)  # 设置动画持续时间
    info_widget_animation_resize.setStartValue(QSize(info_widget.width(), info_widget.height()))  # 初始位置
    info_widget_animation_resize.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    info_widget_animation_resize.setEndValue(
        QSize(
            info_widget.width(),
            info_widget.height() - 206
        )
    )  # 结束位置


    # 添加到动画组
    animation_sequent_group = QParallelAnimationGroup(info_widget)
    animation_sequent_group.addAnimation(info_widget_animation_resize)
    animation_sequent_group.addAnimation(info_widget_animation_move)

    # 输入账密控件,和状态信息控件隐藏
    animation_sequent_group.stateChanged.connect(
        lambda: (account_widget.setHidden(False), status_widget.setHidden(False)))

    # 启动动画
    animation_sequent_group.start()