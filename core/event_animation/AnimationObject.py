#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :AnimationObject.py
# @Time :2023-6-10 下午 10:44
# @Author :Qiao
from typing import Tuple, List

from PyQt5.QtCore import QSize, QPoint, QPropertyAnimation, QEasingCurve, \
    QSequentialAnimationGroup, QParallelAnimationGroup, QAnimationGroup


class Animation:

    def __init__(self, target):
        """
        初始化对象
        :param target: 需要操作的控件
        :param size: 需要设置的大小
        :param time: 动画持续时间(单位:ms)
        :param start_value: 动画开始位置
        :param end_value: 动画结束位置
        :param easing_curve: 缓动曲线设置
        """
        # 接收参数
        self.target = target
        # 初始化参数
        self.animation_group = None

    def setSize(
            self, time: int, easing_curve: QEasingCurve,
            start_value: Tuple[int, int] | QSize | QPoint, end_value: Tuple[int, int] | QSize | QPoint
    ) -> QPropertyAnimation:
        """设置控件大小"""
        # 创建放大动画对象
        widget_resize_animation = QPropertyAnimation(self.target, b'size', self.target)
        # 设置动画持续时间
        widget_resize_animation.setDuration(time)
        # 设置初始位置和结束位置
        self.setAnimationValue(widget_resize_animation, "size", start_value, end_value)
        # 设置动画曲线
        widget_resize_animation.setEasingCurve(easing_curve)
        # 返回动画对象
        return widget_resize_animation

    def setPos(
            self, time: int, easing_curve: QEasingCurve,
            start_value: Tuple[int, int] | QSize | QPoint, end_value: Tuple[int, int] | QSize | QPoint
    ) -> QPropertyAnimation:
        """设置控件位置"""
        # 创建放大动画对象
        widget_resize_animation = QPropertyAnimation(self.target, b'pos', self.target)
        # 设置动画持续时间
        widget_resize_animation.setDuration(time)
        # 设置初始位置和结束位置
        self.setAnimationValue(widget_resize_animation, "pos", start_value, end_value)
        # 设置动画曲线
        widget_resize_animation.setEasingCurve(easing_curve)
        # 返回动画对象
        return widget_resize_animation

    @staticmethod
    def setAnimationValue(
            target: QPropertyAnimation, animation_type: str,
            start_value: Tuple[int, int] | QSize | QPoint, end_value: Tuple[int, int] | QSize | QPoint
    ) -> None:
        """
        设置动画的开始和结束的值
        :param target: 动画对象
        :param animation_type: 动画类型
        :param start_value: 动画初始位置
        :param end_value: 动画结束位置
        """
        if isinstance(start_value, tuple) and isinstance(end_value, tuple) and animation_type == "size":
            target.setStartValue(QSize(start_value[0], start_value[1]))
            target.setEndValue(QSize(end_value[0], end_value[1]))
        elif isinstance(start_value, tuple) and isinstance(end_value, tuple) and animation_type == "pos":
            target.setStartValue(QPoint(start_value[0], start_value[1]))
            target.setEndValue(QPoint(end_value[0], end_value[1]))
        else:
            target.setStartValue(start_value)
            target.setEndValue(end_value)

    def addAnimationGroup(
            self, animation: QPropertyAnimation | List[QPropertyAnimation],
            parallel_mod: bool = False, sequential_mod: bool = False
    ) -> QAnimationGroup:
        """
        添加到动画组中
        :return:
        """
        # 检查参数
        if not parallel_mod and not sequential_mod and self.animation_group is None:
            raise ValueError("parallel_mod和sequential_mod必须选择一个")
        if parallel_mod and sequential_mod:
            raise ValueError("parallel_mod和sequential_mod只能选择一个")

        # 判断模式
        if self.animation_group is None and parallel_mod:
            self.animation_group = QParallelAnimationGroup(self.target)
        if self.animation_group is None and sequential_mod:
            self.animation_group = QSequentialAnimationGroup(self.target)

        # 添加到动画组
        if self.animation_group is None:
            # 类型判断
            raise TypeError("animation_group 类型为 None")
        if isinstance(animation, List):
            [self.animation_group.addAnimation(i) for i in animation]
        elif isinstance(animation, QPropertyAnimation):
            self.animation_group.addAnimation(animation)
        else:
            raise TypeError("animation 的值应该为 QPropertyAnimation 或 List[QPropertyAnimation]")

        return self.animation_group
