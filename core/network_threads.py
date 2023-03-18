#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/4 9:36
# @Author  : 桥话语权
# @File    : network_threads.py
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
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from core.file_operation import FileOperation, VdfOperation
from tcping import Ping
import subprocess


class PingServerThread(QThread):
    sever_signal = pyqtSignal(str)
    end_signal = True

    def __init__(
            self,
            server_icon_label: QLabel,  # 服务器图标
            server_state_label: QLabel,  # 服务器状态图标
            state_label: QLabel,  # 状态标签
            online_state_icon_path: str,  # 服务器在线状态图标路径
            offline_state_icon_path: str,  # 服务器离线状态图标路径
            online_icon_path: str,  # 在线图标路径
            offline_icon_path: str,  # 离线图标路径
            ip: str,  # 服务器
            port: int = 80,  # 端口
            *args,
            **kwargs
    ):
        super(PingServerThread, self).__init__(*args, **kwargs)
        self.server_icon_label: QLabel = server_icon_label
        self.server_state_label: QLabel = server_state_label
        self.state_label: QLabel = state_label
        self.online_state_icon_path: str = online_state_icon_path
        self.offline_state_icon_path: str = offline_state_icon_path
        self.online_icon_path: str = online_icon_path
        self.offline_icon_path: str = offline_icon_path
        self.ip: str = ip
        self.port: int = port

    def run(self):
        while self.end_signal:
            self.sleep(1)
            ping = Ping(self.ip, self.port, 0.5)
            ping.ping(1)
            if '0 successed' in ping.result.raw:
                # 判断是否能ping通,不能则修改为离线状态
                self.modify_to_offline()
            else:
                # 能ping通则修改为在线状态
                self.modify_to_online()
        return

    def modify_to_online(self):
        if self.state_label.text() == '在线':
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
            self.state_label.setText('在线')
            # 返回在线状态
            self.sever_signal.emit(f"{self.state_label.objectName()} : 在线")

    def modify_to_offline(self):
        if self.state_label.text() == '离线':
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
            self.state_label.setText('离线')
            # 返回离线状态
            self.sever_signal.emit(f"{self.state_label.objectName()} : 离线")


class SteamLoginThread(QThread):
    """登录线程"""
    msg = pyqtSignal(str)

    def __init__(
            self, cammy: dict, *args, **kwargs
    ):
        """
        登录线程,cammy参数文档:
            cammy['cammy_user'] - 账号
            cammy['cammy_pwd'] - 密码
            cammy['cammy_ssfn'] - SSFN
            cammy['steam64_id'] - 64id
            cammy['WantsOfflineMode'] - 是否离线模式
            cammy['login_method'] - 登录模式
            cammy['first_login'] - 是否首次登录
        """
        super(SteamLoginThread, self).__init__(*args, **kwargs)
        self.file_path = FileOperation()  # 设置文件路径
        self.user: str = cammy['cammy_user']
        self.pwd: str = cammy['cammy_pwd']
        self.ssfn: str = cammy['cammy_ssfn']
        self.steam64id: str = cammy['steam64_id']
        self.login_method: int = cammy['login_method']
        self.offline: bool = cammy['WantsOfflineMode']

    def run(self):
        if not self.file_path.steam_install_state:
            # 如果没有安装steam,则提示
            self.msg.emit('请先安装steam')
        else:
            self.__determine_login_method()
            self.__determine_login_offline()
            self.__download_ssfn()
            self.__login()

    def __login(self):
        """登录Steam"""
        subprocess.run(
            self.login_method,
            cwd=self.file_path.steam_path
        )

    def __download_ssfn(self):
        """
        下载SSFN
        :return:
        """
        if self.ssfn:
            self.file_path.remove_ssfn()  # 删除SSFN
            with open(self.file_path.steam_path / {self.ssfn}, 'wb') as f:
                f.write(requests.get(f"http://1.15.97.14:8848/ssfn/{self}").content)
        else:
            pass

    def __determine_login_method(self):
        # 设置steam路径
        steam_path = self.file_path.steam_exe_path
        if self.login_method == 0:
            # 正常模式登录
            self.login_method = f"{steam_path} -login {self.user} -password {self.pwd}"
        if self.login_method == 1:
            # 跳过令牌模式登录
            self.login_method = f"{steam_path} -tenfoot -login {self.user} -password {self.pwd}"

    def __determine_login_offline(self):
        """判断是否需要离线"""
        vdf = VdfOperation()
        if self.offline:
            vdf.wants_offline_mode(
                self.file_path.steam_user_path,
                self.steam64id
            )
        else:
            vdf.not_offline_mode(
                self.file_path.steam_user_path,
                self.steam64id
            )
