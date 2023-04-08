#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 12:21
# @Author  : 桥话语权
# @File    : event_judgment.py
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
from core.event_animation import \
    login_account_animation_max, \
    login_account_animation_min, \
    setting_account_animation_max, \
    setting_account_animation_min


def list_widget_icon_color(current: QListWidgetItem, previous: QListWidgetItem) -> None:
    """
    用于修改列表图标显示的颜色
    :param current: 当前列表项
    :param previous: 上一个列表项
    :return:
    """
    # 图标的路径
    icon_path_list = ["./img/icon/item_icon/user.svg", "./img/icon/item_icon/net_acceleration.svg",
                      "./img/icon/item_icon/fun_setting.svg"]
    icon_select_list = ["./img/icon/item_icon/user_select.svg", "./img/icon/item_icon/net_acceleration_select.svg",
                        "./img/icon/item_icon/fun_setting_select.svg"]

    try:
        # 判断现在
        if current.text() == '账号登录':
            current.setIcon(QIcon(icon_select_list[0]))
        if current.text() == '网络加速':
            current.setIcon(QIcon(icon_select_list[1]))
        if current.text() == '功能设置':
            current.setIcon(QIcon(icon_select_list[2]))

        # 判断以前
        if previous.text() == '账号登录':
            previous.setIcon(QIcon(icon_path_list[0]))
        if previous.text() == '网络加速':
            previous.setIcon(QIcon(icon_path_list[1]))
        if previous.text() == '功能设置':
            previous.setIcon(QIcon(icon_path_list[2]))
    except AttributeError:
        return


def login_widget_size_button_checked_event(
        button_state: int,
        info_widget: QWidget,
        account_widget: QWidget,
        status_widget: QWidget
) -> None:
    """
    设置按钮图标,隐藏或显示其他控件

    :param button_state: 按钮状态
    :param info_widget: 信息控件
    :param account_widget: 账号控件
    :param status_widget: 状态控件
    :return:
    """
    if button_state == 0:
        # 如果按钮处于未选中状态
        login_account_animation_min(info_widget, account_widget, status_widget)
    else:
        # 如果按钮处于选中状态
        login_account_animation_max(info_widget, account_widget, status_widget)


def setting_widget_size_button_checked_event(
        button_state: int,
        info_widget: QWidget,
        setting_widget: QWidget,
) -> None:
    """
    设置按钮图标,隐藏或显示其他控件

    :param button_state: 按钮状态
    :param info_widget: 信息控件
    :param setting_widget: 设置控件
    :return:
    """
    print(button_state)
    if button_state == 2:
        # 如果按钮处于未选中状态
        setting_account_animation_max(info_widget, setting_widget)
    else:
        # 如果按钮处于选中状态
        setting_account_animation_min(info_widget, setting_widget)
