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

import subprocess
import winreg
from pathlib import Path

import psutil
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow
from creart import create
from loguru import logger

from core.file_operation import FileOperation
from core.tcping import Ping


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


class SteamLoginThread(QThread):
    """登录线程"""
    msg = pyqtSignal(str)
    login_state = pyqtSignal(bool, str)

    def __init__(
            self, cammy: dict, ui: QMainWindow, *args, **kwargs
    ):
        """
        登录线程,cammy参数文档:
            cammy['cammy_user'] - 账号
            cammy['cammy_pwd'] - 密码
            cammy['cammy_ssfn'] - SSFN
            cammy['skip_email'] - 登录模式
        """
        super(SteamLoginThread, self).__init__(*args, **kwargs)
        self.file_path = create(FileOperation)  # 设置文件路径
        self.user: str = cammy['cammy_user']
        self.pwd: str = cammy['cammy_pwd']
        self.ssfn: str = cammy['cammy_ssfn']
        self.skip_email: bool = cammy['skip_email']
        self.parent: QMainWindow = ui

    def run(self):
        if not self.file_path.steam_install_state:
            # 如果没有安装steam,则提示
            self.msg.emit('请先安装steam')
        else:
            try:
                self.__kill_steam()
                self.__determine_login_method()
                self.__download_ssfn()
                logger.info(f"账号: {self.user} 密码: {self.pwd} SSFN: {self.ssfn} 正在登录")
                logger.info(
                    f"登录参数：{self.file_path.steam_exe_path} -Windowed -noreactlogin -login {self.user} {self.pwd}")
                self.__login()
            except Exception as e:
                logger.error(f"登录失败:\n {e}")

    def __login(self):
        """登录Steam"""
        try:
            subprocess.run(
                f"{self.file_path.steam_exe_path} -Windowed -noreactlogin -login {self.user} {self.pwd}",
                cwd=self.file_path.steam_path
            )
        except FileNotFoundError as e:
            self.login_state.emit(False, f"Steam路径错误,请检查\n当前启动路径:{self.file_path.steam_exe_path}")
        except PermissionError:
            self.login_state.emit(False, "上号器无权访问Steam\n请检查: \n - 杀软是否关闭\n - Steam.exe所在文件夹权限")
        except Exception as e:
            self.login_state.emit(False, f"{e}")

    @staticmethod
    def __kill_steam():
        """结束steam进程"""
        # 获取所有进程列表
        processes = psutil.process_iter()
        # 遍历所有进程
        for proc in processes:
            try:
                # 获取进程名称
                process_name = proc.name()
                # 判断进程是否为Steam
                if process_name == 'steam.exe':
                    # 结束进程
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def __download_ssfn(self):
        """
        下载SSFN
        :return:
        """
        if self.ssfn:
            self.file_path.remove_ssfn()  # 删除SSFN
            with open(Path(self.file_path.steam_path) / self.ssfn, 'wb') as f:
                f.write(requests.get(f"http://1.15.97.14:8848/ssfn/{self.ssfn}").content)
        else:
            pass

    def __determine_login_method(self):
        # 定义要修改的键路径、键名
        key_path = r'Software\Valve\Steam'
        key_name = 'StartupMode'
        if self.skip_email:
            # 跳过令牌模式登录
            key_value = 4
        else:
            # 正常模式登录
            key_value = 0
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)  # 打开注册表键
        winreg.SetValueEx(key, key_name, 0, winreg.REG_DWORD, key_value)  # 修改键值
        winreg.CloseKey(key)  # 关闭注册表键
        logger.info(f"已修改 StartupMode 为： {key_value}")
