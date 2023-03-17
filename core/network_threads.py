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
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from core.file_operation import FileOperation
from tcping import Ping


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
            self,
            user: str,
            pwd: str,
            ssfn: str = '',
            login_method: int = 1,
            offline: bool = False,
            *args, **kwargs
    ):
        """
        登录线程,需要传入以下参数
        user - 账号
        pwd - 密码
        ssfn - 授权(可选)
        login_method - 登录模式
            - 0: 正常模式
            - 1: 跳过令牌(大屏幕模式)
        offline - 是否离线
            - False: 不离线
            - True: 离线
        """
        super(SteamLoginThread, self).__init__(*args, **kwargs)
        self.file_path = FileOperation()  # 设置文件路径
        self.user: str = user
        self.pwd: str = pwd
        self.ssfn: str = ssfn
        self.login_method: int = login_method
        self.offline: bool = offline

    def run(self):
        if not self.file_path.steam_install_state:
            # 如果没有安装steam,则提示
            self.msg.emit('请先安装steam')
        else:
            self.__determine_login_method()


    def __determine_login_method(self):
        # 设置steam路径
        steam_path = self.file_path.steam_exe_path
        if self.login_method == 0:
            # 正常模式登录
            return f"{steam_path} -login {self.user} -password {self.pwd}"
        if self.login_method == 1:
            # 跳过令牌模式登录
            return f"{steam_path} -tenfoot -login {self.user} -password {self.pwd}"

    def __determine_login_offline(self):
        """判断是否需要离线"""
        pass

    def __write_config_file(self):
        """判断配置文件中是否存在,否则写入"""
        path = self.file_path.steam_user_path





