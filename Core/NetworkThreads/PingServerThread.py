#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :PingServerThread.py
# @Time :2023-7-6 下午 07:19
# @Author :Qiao
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from creart import create


class PingServerThread(QThread):
    sever_signal = pyqtSignal(str)
    end_signal = True

    def __init__(self, num: int, parameter_list: list, *args) -> None:
        from Ui.LoginWidget.ServerStateCard import ServerStateCard

        super(PingServerThread, self).__init__(*args)
        self.server_icon_label: QLabel = parameter_list[0][num]
        self.server_state_label: QLabel = parameter_list[1][num]
        self.state_label: QLabel = parameter_list[2][num]
        self.ip: str = parameter_list[3][num]
        self.online_state_icon_path: str = create(ServerStateCard).online_icon[0]
        self.online_icon_path: str = create(ServerStateCard).online_icon[1]
        self.offline_state_icon_path: str = create(ServerStateCard).offline_icon[0]
        self.offline_icon_path: str = create(ServerStateCard).offline_icon[1]

    def run(self) -> None:
        while self.end_signal:
            self.sleep(1)
            # 判断是否能ping通,不能则修改为离线状态
            self.modify_to_online() if self.ping() else self.modify_to_offline()

    def ping(self) -> bool:
        command = ["ping", "-n", "1", "-w", "5000", self.ip]
        # 创建启动信息对象并设置标志位
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # 执行ping命令并返回
        return (
            subprocess.run(
                command, startupinfo=startupinfo, stdout=subprocess.PIPE
            ).returncode
            == 0
        )

    def modify_to_online(self) -> None:
        if self.state_label.text() == "在线":
            # 判断是否要改变,不需要则直接返回
            return
        else:
            # 服务器图标
            self.server_icon_label.setPixmap(QPixmap(self.online_state_icon_path))
            # 服务器状态图标
            self.server_state_label.setFixedSize(14, 14)
            self.server_state_label.setPixmap(QPixmap(self.online_icon_path))
            self.server_state_label.setScaledContents(True)
            # 服务器状态标签
            self.state_label.setText("在线")

    def modify_to_offline(self) -> None:
        if self.state_label.text() == "离线":
            # 判断是否要改变,不需要则直接返回
            return
        else:
            # 服务器图标
            self.server_icon_label.setPixmap(QPixmap(self.offline_state_icon_path))
            # 服务器状态图标
            self.server_state_label.setFixedSize(14, 14)
            self.server_state_label.setPixmap(QPixmap(self.offline_icon_path))
            self.server_state_label.setScaledContents(True)
            # 服务器状态标签
            self.state_label.setText("离线")
