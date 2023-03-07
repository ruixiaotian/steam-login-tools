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
from PyQt5.Qt import *
from pathlib import Path
from core.file_operation import FileOperation
from core.network_threads import PingServerThread
from core.event_judgment import size_button_checked_event

__file_operation = FileOperation()


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
                                account_save_file(
                                    user_edit.text(),
                                    password_edit.text(),
                                    ssfn_edit.text()
                                ))

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

    # 左侧
    scroll_widget = account_info_widget_right()

    # 右侧
    size_button = account_info_widget_left(icon_list, widget, add_account_widget, server_status_widget)

    # 设置控件属性
    widget.resize(540, 200)
    widget.setObjectName('account_info_widget')

    # 添加控件
    layout.addWidget(scroll_widget, 0, 0, 1, 1)
    layout.addWidget(size_button, 0, 1, 1, 1)

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


def account_info_widget_right() -> QWidget:
    """设置左侧的滚动窗体控件"""

    # 创建滚动窗体
    scroll_widget = QScrollArea()
    scroll_widget.setObjectName('scroll_widget')
    scroll_widget.setWidgetResizable(True)

    # 创建滚动窗体内窗体
    scroll_widget_content = QWidget()
    scroll_widget_content.setObjectName('scroll_widget_content')
    scroll_widget_content.resize(540, 200)

    scroll_widget.setWidget(scroll_widget_content)

    return scroll_widget


def scroll_widget_content_setup(account_info: list):
    """
    设置scroll_widget中的账号信息
    :param account_info:
    :return:
    """

    if not account_info:
        # 判断是否有账号信息
        return


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = LoginWidget()
    widget.show()
    sys.exit(app.exec_())
