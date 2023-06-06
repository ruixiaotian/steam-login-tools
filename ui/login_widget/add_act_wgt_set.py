from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QCompleter, \
    QAction
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt

from typing import List
from creart import create

from core.file_operation import FileOperation
from core.network_threads import SteamLoginThread

from ui.share import shadow_setup

__file_operation = create(FileOperation)


def add_account_widget_setup(font: str, refresh: callable):
    """
    设置添加账号的控件

    :return:
    """
    widget = QWidget()
    layout = QGridLayout(widget)

    # 创建控件
    user_edit, password_edit, ssfn_edit = QLineEdit(), QLineEdit(), QLineEdit()
    save_button = QPushButton('保存')
    edit_list = [user_edit, password_edit, ssfn_edit]

    # 创建列表
    edit_obj_name_list = ['user_edit', 'password_edit', 'ssfn_edit']
    place_text_list = ['USER-账号', 'PASSWORD-密码', 'SSFN(如果有)']
    icon_path_list = [
        './img/icon/login_widget/add_account/user.svg',
        './img/icon/login_widget/add_account/pwd.svg',
        './img/icon/login_widget/add_account/ssfn.svg'
    ]

    # 单独设置属性
    widget.setObjectName('add_account_widget')  # 设置控件的名字
    save_button.setObjectName("save_button")
    save_button.setFixedSize(100, 30)
    save_button.setFont(QFont(font, 11))
    password_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码输入模式
    # 设置可见与不可见切换和联想器
    __pwd_edit_toggles_visible_state(password_edit)
    __ssfn_edit_completer(ssfn_edit)

    # 循环设置对象名称
    for edit, name in zip(edit_list, edit_obj_name_list):
        edit.setObjectName(name)  # 设置对象名称
        edit.setClearButtonEnabled(True)  # 设置清除按钮

    # 循环设置属性
    for edit, text in zip(edit_list, place_text_list):
        # 设置输入框通用属性
        edit.setFixedSize(200, 30)
        edit.setPlaceholderText(text)
        edit.setFont(QFont(font, 8))
    for edit, path in zip(edit_list, icon_path_list):
        # 循环设置输入款图标
        edit.addAction(QIcon(path), QLineEdit.LeadingPosition)

    """绑定按钮信号"""
    # 保存按钮
    save_button.clicked.connect(
        lambda: __save_button_trough(
            refresh, user_edit, password_edit, ssfn_edit
        )
    )

    # 添加到布局
    __add_layout(
        layout,
        [user_edit, password_edit, ssfn_edit, save_button],
        [Qt.AlignHCenter for i in range(4)]
    )

    # 设置阴影
    shadow_setup(
        widget, (2, 3), 25, QColor(29, 190, 245, 80)
    )

    return widget


def __save_button_trough(
        refresh: callable, user_edit: QLineEdit,
        pwd_edit: QLineEdit, ssfn_edit: QLineEdit
) -> None:
    """保存按钮的槽函数"""
    if user_edit.text() and pwd_edit.text() != str():
        __account_save_file(user_edit.text(), pwd_edit.text(), ssfn_edit.text())
        refresh()
        user_edit.clear()
        pwd_edit.clear()
        ssfn_edit.clear()


def __add_layout(
        layout: QGridLayout, widget: List[QLineEdit], layout_policy: List[Qt]
) -> None:
    """添加到布局"""
    layout.setContentsMargins(4, 35, 0, 20)

    for num, edit, policy in zip(range(widget.__len__()), widget, layout_policy):
        layout.addWidget(edit, num, 0, 1, 1, policy)


def __pwd_edit_toggles_visible_state(pwd_edit: QLineEdit):
    """密码编辑框模式切换槽函数"""

    def judgement():
        # 定义判断函数
        if pwd_edit.echoMode() == QLineEdit.PasswordEchoOnEdit:
            # 如果是密码输入模式,则切换回普通模式
            pwd_edit.setEchoMode(QLineEdit.Normal)  # 设置普通模式
            action.setIcon(QIcon('./img/icon/login_widget/add_account/invisible.svg'))
        else:
            # 如果是普通输入模式,则切换回密码输入模式
            pwd_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码模式
            action.setIcon(QIcon('./img/icon/login_widget/add_account/visible.svg'))

    # 设置行为
    action = QAction(pwd_edit)
    action.setIcon(QIcon('./img/icon/login_widget/add_account/visible.svg'))
    action.triggered.connect(judgement)

    # 添加到输入框
    pwd_edit.addAction(action, QLineEdit.TrailingPosition)


def __ssfn_edit_completer(ssfn_edit: QLineEdit):
    """ssfn自动补全槽函数"""
    # 创建一个字符串列表作为 自动补全 的候选项
    ssfn_list = __file_operation.read_json_file('./data/ssfn_list.json')
    # 创建一个 QCompleter 对象，并将字符串列表设置为其自动补全的候选项
    completer = QCompleter(ssfn_list, ssfn_edit)
    completer.setObjectName("ssfn_edit_completer")
    completer.setCompletionMode(QCompleter.InlineCompletion)  # 设置自动补全模式
    # 将 QCompleter 对象设置为 QLineEdit 的自动补全器
    ssfn_edit.setCompleter(completer)


def __account_save_file(user: str, pwd: str, ssfn: str = str()):
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

    __file_operation.modify_json(
        __file_operation.cammy_data_path, config, add=True
    )
