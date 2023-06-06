from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap
from PyQt5.QtCore import Qt

from typing import List

from ui.share import shadow_setup
from core.network_threads import PingServerThread


def server_status_widget_setup(
        font: str, ui: QMainWindow, pings: list | None
) -> QWidget:
    """
    设置服务器状态的控件
    """
    """"创建控件"""
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置属性
    widget.resize(400, 500)
    widget.setObjectName('server_status_widget')

    # 图标路径
    online_icon = [
        './img/icon/login_widget/server_status/server_normal.svg',  # 服务器在线图标
        './img/icon/login_widget/server_status/online.png'  # 在线状态图标
    ]
    offline_icon = [
        './img/icon/login_widget/server_status/server_error.svg',  # 服务器离线图标
        './img/icon/login_widget/server_status/offline.png'  # 离线状态图标
    ]

    # 添加图标
    online_server_icon, online_icon_list = [online_icon[0] for _ in range(3)], [online_icon[1] for _ in range(3)]
    offline_server_icon, offline_icon_list = [offline_icon[0] for _ in range(3)], [offline_icon[1] for _ in range(3)]

    # 服务器IP列表
    server_ip_list = [
        '1.15.97.14', 'wp.qiao.icu', 'wp.qiao.icu'
    ]
    port_list = [
        8848, 80, 80
    ]

    # 创建控件列表
    server_icon_label_list = [QLabel() for _ in range(3)]
    server_num_label_list = [QLabel() for _ in range(3)]
    server_status_icon_list = [QLabel() for _ in range(3)]
    server_status_label_list = [QLabel() for _ in range(3)]

    # 循环设置控件

    for label in server_icon_label_list:
        # 设置图标
        label.setPixmap(QPixmap(online_icon[0]))  # 服务器在线图标

    for num, label in enumerate(server_num_label_list, 1):
        # 设置服务器编号和字体
        label.setText(f"授权服务器 {num} 号")
        label.setFont(QFont(font, 10))

    for label in server_status_icon_list:
        # 设置大小
        label.setFixedSize(14, 14)
        # 设置图标
        label.setPixmap(QPixmap(online_icon[1]))  # 在线图标
        # 设置自动缩放
        label.setScaledContents(True)

    for label in server_status_label_list:
        # 设置显示内容和字体
        label.setText('在线')
        label.setFont(QFont(font, 10))

    """功能实现"""
    zip_list = zip(  # zip函数单独取出来增加可读性
        server_icon_label_list, server_status_icon_list, server_status_label_list,
        online_server_icon, offline_server_icon, online_icon_list, offline_icon_list,
        server_ip_list, port_list
    )
    __start_pings(zip_list, pings, ui)

    """布局实现"""
    __add_layout(
        layout,
        [
            server_icon_label_list, server_num_label_list,
            server_status_icon_list, server_status_label_list
        ]
    )

    # 设置阴影
    shadow_setup(
        widget, (2, 3), 25, QColor(29, 190, 245, 80)
    )

    return widget


def __start_pings(zip_list: zip, pings: list, ui: QMainWindow):
    """循环启动线程"""
    for server_label_icon, server_state_label, state_label, online_state_icon, \
            offline_state_icon, online_icon, offline_icon, ip, port in zip_list:
        # 循环启动Ping线程
        ping = PingServerThread(
            server_label_icon, server_state_label, state_label,
            online_state_icon, offline_state_icon, online_icon,
            offline_icon, ip, port, ui
        )
        ping.start()
        pings.append(ping)

def __add_layout(layout: QGridLayout, wgt_list: list):
    """
    添加到布局
    :return:
    """

    # 循环添加到布局
    for num, label in enumerate(wgt_list[0], 1):
        # 将服务器状态图标添加到布局
        layout.addWidget(label, num, 0, 1, 1)

    for num, label in enumerate(wgt_list[1], 1):
        # 将服务器编号添加到布局
        layout.addWidget(label, num, 1, 1, 1)

    for num, label in enumerate(wgt_list[2], 1):
        # 将状态图标添加到布局
        layout.addWidget(label, num, 2, 1, 1)

    for num, label in enumerate(wgt_list[3], 1):
        # 将服务器状态添加到布局
        layout.addWidget(label, num, 3, 1, 1)

    # 设置布局边距
    layout.setContentsMargins(55, 0, 60, 0)
    layout.setSpacing(5)
