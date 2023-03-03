#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 16:23
# @Author  : 桥话语权
# @File    : login_widget.py
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


def login_widget_setup(font: str):
    """
    设置登录界面
    :param font:
    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 500)
    widget.setObjectName('login_widget')

    # 添加控件
    layout.addWidget(title_widget_setup(font), 0, 0, 1, 2)
    layout.addWidget(add_account_widget_setup(font), 1, 0, 1, 1)
    layout.addWidget(server_status_widget_setup(font), 1, 1, 1, 1)
    layout.addWidget(account_info_widget_setup(font), 2, 0, 1, 2)

    return widget


def title_widget_setup(font: str):
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.setFixedSize(400, 50)
    widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    # 添加控件
    label = QLabel('Login')
    label.setFont(QFont(font, 16))
    label.setObjectName('title_label')
    layout.addWidget(label, 0, 0, 1, 1, Qt.AlignLeft)
    layout.setContentsMargins(0, 0, 0, 0)

    return widget


def add_account_widget_setup(font: str):
    widget = QWidget()
    layout = QGridLayout(widget)

    # 创建控件
    user_edit = QLineEdit()
    password_edit = QLineEdit()
    ssfn_edit = QLineEdit()
    login_button = QPushButton('登录')
    save_button = QPushButton('保存')
    edit_list = [user_edit, password_edit, ssfn_edit]
    btn_list = [login_button, save_button]

    # 创建列表
    edit_obj_name_list = ['user_edit', 'password_edit', 'ssfn_edit']
    btn_obj_name_list = ['login_button', 'save_button']
    place_text_list = ['USER-账号', 'PASSWORD-密码', 'SSFN(如果有)']
    icon_path_list = ['./img/icon/add_account/user.svg', './img/icon/add_account/pwd.svg',
                      './img/icon/add_account/ssfn.svg']
    # 循环设置对象名称
    for edit, name in zip(edit_list, edit_obj_name_list):
        edit.setObjectName(name)
    for btn, name in zip(btn_list, btn_obj_name_list):
        btn.setObjectName(name)

    # 单独设置属性
    widget.setObjectName('add_account_widget')
    # 循环设置属性
    for edit, text in zip(edit_list, place_text_list):
        # 设置输入框通用属性
        edit.setFixedSize(200, 30)
        edit.setPlaceholderText(text)
        edit.setFont(QFont(font, 8))
    for edit, path in zip(edit_list, icon_path_list):
        # 循环设置输入款图标
        edit_icon_setup(edit, path)

    for btn in btn_list:
        # 设置按钮通用属性
        btn.setFixedSize(80, 35)
        btn.setFont(QFont(font, 11))

    # 添加到布局
    layout.setContentsMargins(0, 30, 0, 20)

    layout.addWidget(user_edit, 0, 0, 1, 2, Qt.AlignCenter)
    layout.addWidget(password_edit, 1, 0, 1, 2, Qt.AlignCenter)
    layout.addWidget(ssfn_edit, 2, 0, 1, 2, Qt.AlignCenter)
    layout.addWidget(save_button, 3, 0, 1, 1, Qt.AlignRight)
    layout.addWidget(login_button, 3, 1, 1, 1, Qt.AlignLeft)

    # 设置阴影
    shadow_setup(widget)

    return widget


def server_status_widget_setup(font: str):
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 500)
    widget.setObjectName('server_status_widget')

    # 添加控件

    # 设置阴影
    shadow_setup(widget)

    return widget


def account_info_widget_setup(font: str):
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 200)
    widget.setObjectName('account_info_widget')

    # 添加控件

    # 设置阴影
    shadow_setup(widget)

    return widget


def shadow_setup(target: QWidget):
    # 设置阴影
    effect_shadow = QGraphicsDropShadowEffect(target)
    effect_shadow.setOffset(2, 3)  # 阴影的偏移量
    effect_shadow.setBlurRadius(25)  # 阴影的模糊程度
    effect_shadow.setColor(QColor(29, 190, 245, 80))  # 阴影的颜色
    target.setGraphicsEffect(effect_shadow)


def edit_icon_setup(target: QLineEdit, path: str):
    """
    设置输入框的图标
    :param target:
    :param path:
    :return:
    """
    action = QAction(target)
    action.setIcon(QIcon(path))
    target.addAction(action, QLineEdit.LeadingPosition)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LoginWidget()
    widget.show()
    sys.exit(app.exec_())
