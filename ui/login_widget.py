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
import json
import datetime
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QGridLayout, QCheckBox, QAction, QSizePolicy, QCompleter, QGraphicsDropShadowEffect, QScrollArea, QMenu, \
    QSpacerItem
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPainter
from PyQt5.QtCore import Qt
from pathlib import Path
from core.file_operation import FileOperation
from core.network_threads import PingServerThread
from core.event_judgment import size_button_checked_event

__file_operation = FileOperation()

scroll_widget = None
content = None


def login_widget_setup(font: str, ui: QMainWindow):
    """
    设置登录界面
    :param font:
    :param ui:
    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 500)
    widget.setObjectName('login_widget')

    # 获取控件
    title_widget = title_widget_setup(font)
    add_account_widget = add_account_widget_setup(font)
    server_status_widget, pings = server_status_widget_setup(font, ui)
    account_info_widget = account_info_widget_setup(font, add_account_widget, server_status_widget)
    # 添加控件
    layout.addWidget(title_widget, 0, 0, 1, 2)
    layout.addWidget(add_account_widget, 1, 0, 1, 1)
    layout.addWidget(server_status_widget, 1, 1, 1, 1)
    layout.addWidget(account_info_widget, 2, 0, 1, 2)

    return widget, pings


def title_widget_setup(font: str):
    """
    设置顶部标题的控件

    :param font:
    :return:
    """
    # 创建控件
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
    """
    设置添加账号的控件

    :param font:
    :return:
    """
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

    # 单独设置属性
    widget.setObjectName('add_account_widget')  # 设置控件的名字
    edit_list[1].setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码输入模式
    # 设置可见与不可见切换和联想器
    pwd_edit_toggles_visible_state(edit_list[1])
    ssfn_edit_completer(edit_list[2])

    # 循环设置对象名称
    for edit, name in zip(edit_list, edit_obj_name_list):
        edit.setObjectName(name)  # 设置对象名称
        edit.setClearButtonEnabled(True)  # 设置清除按钮
    for btn, name in zip(btn_list, btn_obj_name_list):
        btn.setObjectName(name)  # 设置对象名称

    # 循环设置属性
    for edit, text in zip(edit_list, place_text_list):
        # 设置输入框通用属性
        edit.setFixedSize(200, 30)
        edit.setPlaceholderText(text)
        edit.setFont(QFont(font, 8))
    for edit, path in zip(edit_list, icon_path_list):
        # 循环设置输入款图标
        edit.addAction(QIcon(path), QLineEdit.LeadingPosition)

    for btn in btn_list:
        # 设置按钮通用属性
        btn.setFixedSize(80, 35)
        btn.setFont(QFont(font, 11))

    # 绑定按钮信号
    save_button.clicked.connect(lambda:
                                (
                                    account_save_file(
                                        user_edit.text(),
                                        password_edit.text(),
                                        ssfn_edit.text()
                                    ),
                                    refresh_widget(
                                        font
                                    )
                                )
                                )

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


def server_status_widget_setup(font: str, ui: QMainWindow):
    """
    设置服务器状态的控件

    :param font:
    :param ui:
    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 500)
    widget.setObjectName('server_status_widget')

    # 图标路径
    online_icon = [
        './img/icon/server_status/server_normal.svg',  # 服务器在线图标
        './img/icon/server_status/online.png'  # 在线状态图标
    ]
    offline_icon = [
        './img/icon/server_status/server_error.svg',  # 服务器离线图标
        './img/icon/server_status/offline.png'  # 离线状态图标
    ]
    online_server_icon = [
        online_icon[0],
        online_icon[0],
        online_icon[0]
    ]
    online_icon_list = [
        online_icon[1],
        online_icon[1],
        online_icon[1],
    ]
    offline_server_icon = [
        offline_icon[0],
        offline_icon[0],
        offline_icon[0],
    ]
    offline_icon_list = [
        offline_icon[1],
        offline_icon[1],
        offline_icon[1],
    ]
    # 服务器IP列表
    server_ip_list = [
        '1.15.97.14',
        'wp.qiao.icu',
        'wp.qiao.icu'
    ]
    port_list = [
        8848,
        80,
        80
    ]

    # 创建控件
    server_icon_label_list = [QLabel(), QLabel(), QLabel()]
    server_num_label_list = [QLabel(), QLabel(), QLabel()]
    server_status_icon_list = [QLabel(), QLabel(), QLabel()]
    server_status_label_list = [QLabel(), QLabel(), QLabel()]

    # 循环设置控件
    for label, num in zip(server_icon_label_list, range(1, 4)):
        # 设置图标
        label.setPixmap(QPixmap(online_icon[0]))  # 服务器在线图标
        # 设置对象名称
        label.setObjectName(f'server_icon_label_{num}')

    for label, num in zip(server_num_label_list, range(1, 4)):
        # 设置服务器编号和字体
        label.setText(f"授权服务器 {num}号")
        label.setFont(QFont(font, 10))
        # 设置对象名称
        label.setObjectName(f'server_num_label_{num}')

    for label, num in zip(server_status_icon_list, range(1, 4)):
        # 设置大小
        label.setFixedSize(14, 14)
        # 设置图标
        label.setPixmap(QPixmap(online_icon[1]))  # 在线图标
        # 设置自动缩放
        label.setScaledContents(True)
        # 设置对象名称
        label.setObjectName(f'server_status_icon_{num}')

    for label, num in zip(server_status_label_list, range(1, 4)):
        # 设置显示内容和字体
        label.setText('在线')
        label.setFont(QFont(font, 10))
        # 设置对象名称
        label.setObjectName(f'server_status_label_{num}')

    pings = []  # 创建线程列队
    for server_label_icon, server_state_label, state_label, online_state_icon, offline_state_icon, online_icon, offline_icon, ip, port in zip(
            server_icon_label_list,
            server_status_icon_list,
            server_status_label_list,
            online_server_icon,
            offline_server_icon,
            online_icon_list,
            offline_icon_list,
            server_ip_list,
            port_list
    ):
        ping = PingServerThread(
            server_label_icon,
            server_state_label,
            state_label,
            online_state_icon,
            offline_state_icon,
            online_icon,
            offline_icon,
            ip,
            port,
            ui
        )
        ping.sever_signal.connect(print)
        ping.start()
        pings.append(ping)

    # 添加到布局
    for label, num in zip(server_icon_label_list, range(1, 4)):
        # 将服务器状态图标添加到布局
        layout.addWidget(label, num, 0, 1, 1)

    for label, num in zip(server_num_label_list, range(1, 4)):
        # 将服务器编号添加到布局
        layout.addWidget(label, num, 1, 1, 1)

    for label, num in zip(server_status_icon_list, range(1, 4)):
        # 将状态图标添加到布局
        layout.addWidget(label, num, 2, 1, 1)

    for label, num in zip(server_status_label_list, range(1, 4)):
        # 将服务器状态添加到布局
        layout.addWidget(label, num, 3, 1, 1)

    # 设置布局边距
    layout.setContentsMargins(55, 0, 60, 0)
    layout.setSpacing(5)

    # 设置阴影
    shadow_setup(widget)

    return widget, pings


def account_info_widget_setup(font: str, add_account_widget, server_status_widget):
    """
    设置账号信息的控件

    :param font:
    :param add_account_widget:
    :param server_status_widget:
    :return:
    """
    # 创建控件
    widget = QLabel()
    layout = QGridLayout(widget)

    # 图标路径
    icon_list = [
        './img/icon/account_info/size_button_unchecked.svg',
        './img/icon/account_info/size_button_checked.svg'
    ]

    # 右侧
    global scroll_widget, content
    scroll_widget, content = account_info_widget_right(font)

    # 左侧
    size_button = account_info_widget_left(icon_list, widget, add_account_widget, server_status_widget)

    # 设置控件属性
    widget.resize(540, 220)
    widget.setObjectName('account_info_widget')

    # 添加控件
    layout.addWidget(scroll_widget, 0, 0, 1, 1)
    layout.addWidget(size_button, 0, 1, 1, 1, Qt.AlignTop)

    # 设置阴影
    shadow_setup(widget)

    return widget


def account_info_widget_left(icon_list, widget, add_account_widget, server_status_widget) -> QCheckBox:
    """
    设置右侧的放大/缩小控件
    :param icon_list:  图标列表
    :param widget:  承载窗体
    :param add_account_widget:  添加账号的控件
    :param server_status_widget:  服务器状态的控件
    :return:
    """
    size_button = QCheckBox()

    # 单独设置属性
    # 放大_缩小按钮设置, 绑定事件
    size_button.setObjectName('size_button')
    size_button.setFixedSize(32, 32)
    # int类型 当选中时为2,未选中时为0
    size_button.stateChanged.connect(
        lambda state:
        size_button_checked_event(
            size_button,
            icon_list,
            state,
            widget,
            add_account_widget,
            server_status_widget
        )
    )

    return size_button


def account_info_widget_right(font: str) -> QWidget:
    """设置右侧的滚动窗体控件"""

    # 创建滚动窗体
    scroll_widget = QScrollArea()
    scroll_widget.setObjectName('scroll_widget')
    scroll_widget.setWidgetResizable(True)

    # 创建滚动窗体内窗体
    scroll_widget_content = loop_add_widget(font)
    scroll_widget_content.setObjectName('scroll_widget_content')
    scroll_widget_content.resize(540, 220)

    scroll_widget.setWidget(scroll_widget_content)

    return scroll_widget, scroll_widget_content


def loop_add_widget(font: str) -> QWidget:
    """
    循环添加控件
    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)

    account: list = __file_operation.read_json()  # 读取账号信息
    for i, num in zip(account, range(len(account))):
        # 循环创建控件
        layout.addWidget(scroll_widget_card_setup(font, i), num, 0, 1, 1, Qt.AlignTop)

    layout.addItem(QSpacerItem(1000, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding), len(account) + 1, 0, 1, 1)

    layout.setContentsMargins(10, 1, 0, 0)
    layout.setSpacing(0)

    return widget


def scroll_widget_card_setup(font: str, account: dict) -> QWidget:
    """
    设置滚动窗体内卡片控件
    :param font:
    :param account:
    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)
    # 设置控件属性
    widget.setObjectName("scroll_widget_card")
    widget.setFixedSize(435, 85)

    # 设置头像
    avatar_img = __scroll_widget_card_avatar_img(account)
    # 设置显示名称
    avatar_name = __scroll_widget_card_avatar_name(account, font)
    # 账号属性: 最近登录, 离线模式
    recently_logged = __scroll_widget_card_recently_logged(font)
    offline_logged = __scroll_widget_card_offline(font)
    # 登录时间
    time = __scroll_widget_card_time(account, font)
    # 更多按钮
    other_btn = __scroll_widget_card_other_btn(account, font)

    # 判断控件是否可见
    __determine_account_attributes(account, recently_logged, offline_logged)

    # 添加到控件
    layout.addWidget(avatar_img, 0, 0, 4, 1)
    layout.addWidget(avatar_name, 0, 1, 1, 1)
    layout.addWidget(recently_logged, 1, 1, 1, 1)
    layout.addWidget(offline_logged, 1, 2, 1, 1)
    layout.addWidget(time, 3, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)
    layout.addWidget(other_btn, 0, 5, 1, 1)

    # 添加弹簧
    layout.addItem(QSpacerItem(1000, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 3, 1, 1)
    layout.addItem(QSpacerItem(1000, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 4, 1, 1)
    layout.addItem(QSpacerItem(25, 1, QSizePolicy.Minimum, QSizePolicy.Minimum), 1, 5, 1, 1)
    layout.addItem(QSpacerItem(1, 2, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding), 2, 1, 1, 1)

    # 设置弹簧
    layout.setContentsMargins(0, 6, 0, 6)

    layout.setVerticalSpacing(7)

    return widget


def __scroll_widget_card_avatar_img(account_info: dict) -> QLabel:
    """设置账号头像的控件"""
    img = QLabel()
    img.setPixmap(QPixmap(account_info['img_path']))
    img.setFixedSize(75, 75)
    img.setObjectName('avatar_img')
    img.setScaledContents(True)

    return img


def __scroll_widget_card_avatar_name(account_info: dict, font: str) -> QWidget:
    """设置账号名称的控件"""
    widget = QWidget()  # 承载窗体
    layout = QGridLayout(widget)  # 创建布局

    # 创建控件
    label = QLabel()
    name_label = QLabel(account_info['cammy_user'])

    # 设置窗体属性
    widget.setFixedSize(300, 20)

    # 设置图标属性
    label.setFixedSize(16, 16)
    label.setObjectName('account_img_label')
    label.setPixmap(QPixmap("./img/icon/account_info/account_name_icon.svg"))
    label.setScaledContents(True)

    # 设置名字属性
    name_label.setFixedSize(name_label.width(), 20)
    name_label.setObjectName('account_name_label')
    name_label.setFont(QFont(font, 11))

    # 添加到控件
    layout.addWidget(label, 0, 0, 1, 1)
    layout.addWidget(name_label, 0, 1, 1, 1)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.setHorizontalSpacing(5)

    return widget


def __scroll_widget_card_recently_logged(font: str) -> QWidget:
    """
    设置卡片显示的最近登录
    :param account_info:
    :param font:
    :return:
    """
    widget = QWidget()  # 承载窗体
    layout = QGridLayout(widget)  # 创建布局

    # 创建控件
    img = QLabel()
    label = QLabel("最近登录")

    # 设置窗体属性
    widget.setObjectName("account_attributes")
    widget.setFixedSize(80, 25)

    # 设置图标属性
    img.setFixedSize(16, 16)
    img.setObjectName('recently_logged')
    img.setPixmap(QPixmap("./img/icon/account_info/recently_logged_icon.svg"))
    img.setScaledContents(True)

    # 设置名字属性
    label.setFixedSize(55, 24)
    label.setObjectName('recently_logged')
    label.setFont(QFont(font, 9))

    # 添加到控件
    layout.addWidget(img, 0, 0, 1, 1)
    layout.addWidget(label, 0, 1, 1, 1)
    layout.setContentsMargins(5, 0, 0, 0)
    layout.setSpacing(0)
    layout.setHorizontalSpacing(5)

    return widget


def __scroll_widget_card_offline(font: str) -> QWidget:
    """
    设置卡片显示的最近登录
    :param account_info:
    :param font:
    :return:
    """
    widget = QWidget()  # 承载窗体
    layout = QGridLayout(widget)  # 创建布局

    # 创建控件
    img = QLabel()
    label = QLabel("离线模式")

    # 设置窗体属性
    widget.setObjectName("account_attributes")
    widget.setFixedSize(80, 25)

    # 设置图标属性
    img.setFixedSize(16, 16)
    img.setObjectName('offline_logged')
    img.setPixmap(QPixmap("./img/icon/account_info/offline_logged_icon.svg"))
    img.setScaledContents(True)

    # 设置名字属性
    label.setFixedSize(55, 24)
    label.setObjectName('offline_logged')
    label.setFont(QFont(font, 9))

    # 添加到控件
    layout.addWidget(img, 0, 0, 1, 1)
    layout.addWidget(label, 0, 1, 1, 1)
    layout.setContentsMargins(5, 0, 0, 0)
    layout.setSpacing(0)
    layout.setHorizontalSpacing(5)

    return widget


def __scroll_widget_card_time(account_info: dict, font: str) -> QWidget:
    """
    设置登录时间的控件
    :param font:
    :return:
    """
    widget = QWidget()  # 承载窗体
    layout = QGridLayout(widget)  # 创建布局

    if not account_info['Timestamp']:
        time = "暂未登录"
    else:
        # 时间戳转换
        time = datetime.datetime.fromtimestamp(int(account_info['Timestamp'])).strftime("%Y-%m-%d %H:%M:%S")

    # 创建控件
    img = QLabel()
    label = QLabel(time)

    # 设置窗体属性
    widget.setObjectName("logged_time_widget")
    widget.setFixedSize(155, 14)

    # 设置图标属性
    img.setFixedSize(14, 14)
    img.setObjectName('logged_time')
    img.setPixmap(QPixmap("./img/icon/account_info/time_icon.svg"))
    img.setScaledContents(True)

    # 设置名字属性
    label.setFixedSize(155, 14)
    label.setObjectName('logged_time')
    label.setFont(QFont(font, 8))

    # 添加到控件
    layout.addWidget(img, 0, 0, 1, 1)
    layout.addWidget(label, 0, 1, 1, 1)

    layout.setContentsMargins(0, 0, 0, 5)
    layout.setHorizontalSpacing(5)

    return widget


def __scroll_widget_card_other_btn(account_info: dict, font: str) -> QPushButton:
    """
    设置卡片上的其他按钮
    :param account_info:
    :param font:
    :return:
    """
    # 创建控件
    btn = QPushButton()
    btn.setIcon(QIcon("./img/icon/account_info/other_btn_icon.svg"))
    btn.setFixedSize(24, 24)
    btn.setObjectName('other_btn')

    # 创建菜单
    menu = QMenu(btn)
    menu.setFixedSize(115, 135)

    # 创建菜单项
    menu_login_btn = QAction(QIcon('./img/icon/account_info/action_login_btn.svg'), "登录账号", menu)
    menu_edit_btn = QAction(QIcon('./img/icon/account_info/action_edit_btn.svg'), "修改账号", menu)
    menu_delete_btn = QAction(QIcon('./img/icon/account_info/action_delete_btn.svg'), "删除账号", menu)
    menu_offline_login_btn = QAction(QIcon('./img/icon/account_info/other_btn_menu_offline_false.svg'), '离线登录',
                                     menu)

    # 菜单项列表
    menu_list = [
        menu_login_btn,
        menu_edit_btn,
        menu_delete_btn,
        menu_offline_login_btn,
    ]

    # 设置菜单
    menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
    menu.setAttribute(Qt.WA_TranslucentBackground)
    # 设置菜单项可选
    menu_offline_login_btn.setCheckable(True)

    # 循环设置控件
    for i in menu_list:
        i.setFont(QFont(font, 12))  # 设置字体
        menu.addAction(i)  # 添加到菜单

    # 菜单项槽函数绑定
    menu_offline_login_btn.triggered.connect(
        lambda: other_btn_menu_offline_action(menu_offline_login_btn, account_info))

    # 设置控件对象名称
    menu.setObjectName('other_btn_menu')

    # 给菜单添加阴影
    shadow = QGraphicsDropShadowEffect(menu)  # 创建阴影效果对象
    shadow.setOffset(3, 2)  # 阴影的偏移量
    shadow.setColor(QColor(29, 190, 245, 0))  # 阴影的颜色
    menu.setGraphicsEffect(shadow)  # 设置阴影效果

    # 设置按钮菜单
    btn.setMenu(menu)

    return btn


def __determine_account_attributes(
        account_info: dict,
        recently_logged: QWidget,
        offline_logged: QWidget
):
    """
    判断属性是否要显示
    :param account_info:
    :return:
    """
    if account_info['MostRecent'] != '1':
        # 判断是否为最近登录
        recently_logged.setHidden(True)
    if account_info['WantsOfflineMode'] != '1':
        # 判断是否为离线模式
        offline_logged.setHidden(True)


def shadow_setup(target: QWidget):
    # 设置阴影
    effect_shadow = QGraphicsDropShadowEffect(target)  # 创建阴影效果对象
    effect_shadow.setOffset(2, 3)  # 阴影的偏移量
    effect_shadow.setBlurRadius(25)  # 阴影的模糊程度
    effect_shadow.setColor(QColor(29, 190, 245, 80))  # 阴影的颜色
    target.setGraphicsEffect(effect_shadow)  # 设置阴影效果


def account_save_file(user: str, pwd: str, ssfn: str = ''):
    """
    保存按钮槽函数
    :param user:
    :param pwd:
    :param ssfn:
    :return:
    """
    config = __file_operation.template
    config['cammy_user'] = user
    config['cammy_pwd'] = pwd
    config['cammy_ssfn'] = ssfn
    print(config)

    __file_operation.modify_json(config, add=True)


def pwd_edit_toggles_visible_state(pwd_edit: QLineEdit):
    def judgement():
        # 定义判断函数
        if pwd_edit.echoMode() == QLineEdit.PasswordEchoOnEdit:
            # 如果是密码输入模式,则切换回普通模式
            pwd_edit.setEchoMode(QLineEdit.Normal)  # 设置普通模式
            action.setIcon(QIcon('./img/icon/add_account/invisible.svg'))
        else:
            # 如果是普通输入模式,则切换回密码输入模式
            pwd_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码模式
            action.setIcon(QIcon('./img/icon/add_account/visible.svg'))

    # 设置行为
    action = QAction(pwd_edit)
    action.setIcon(QIcon('./img/icon/add_account/visible.svg'))
    action.triggered.connect(judgement)

    # 添加到输入框
    pwd_edit.addAction(action, QLineEdit.TrailingPosition)


def ssfn_edit_completer(ssfn_edit: QLineEdit):
    # 创建一个字符串列表作为自动补全的候选项
    with open('./data/ssfn_list.json', 'r', encoding='utf-8') as f:
        ssfn_list = json.load(f)
    # 创建一个 QCompleter 对象，并将字符串列表设置为其自动补全的候选项
    completer = QCompleter(ssfn_list, ssfn_edit)
    completer.setObjectName("ssfn_edit_completer")
    completer.setCompletionMode(QCompleter.InlineCompletion)  # 设置自动补全模式
    # 将 QCompleter 对象设置为 QLineEdit 的自动补全器
    ssfn_edit.setCompleter(completer)


def other_btn_menu_offline_action(action: QAction, account_info: dict):
    """
    其他按钮中离线登录复选框的槽函数
    :param action:
    :return:
    """
    if action.isChecked():
        action.setIcon(QIcon('./img/icon/account_info/other_btn_menu_offline_true.svg'))
    else:
        action.setIcon(QIcon('./img/icon/account_info/other_btn_menu_offline_false.svg'))


def refresh_widget(font):
    """
    刷新窗体
    :param font:
    :return:
    """
    global scroll_widget, content
    content = loop_add_widget(font)
    content.setObjectName('scroll_widget_content')
    content.resize(540, 220)
    scroll_widget.setWidget(content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LoginWidget()
    widget.show()
    sys.exit(app.exec_())
