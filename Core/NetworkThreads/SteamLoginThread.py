#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :SteamLoginThread.py
# @Time :2023-7-6 下午 07:19
# @Author :Qiao
import subprocess
import winreg
from pathlib import Path

import psutil
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from creart import create
from loguru import logger

from Core.FileOperation import FileOperation


class SteamLoginThread(QThread):
    """登录线程"""

    msg = pyqtSignal(str)
    login_state = pyqtSignal(bool, str)

    def __init__(self, cammy: dict, ui: QMainWindow, *args, **kwargs) -> None:
        """
        登录线程,cammy参数文档:
            cammy['cammy_user'] - 账号
            cammy['cammy_pwd'] - 密码
            cammy['cammy_ssfn'] - SSFN
            cammy['skip_email'] - 登录模式
        """
        super(SteamLoginThread, self).__init__(*args, **kwargs)
        self.file_path = create(FileOperation)  # 设置文件路径
        self.user: str = cammy["cammy_user"]
        self.pwd: str = cammy["cammy_pwd"]
        self.ssfn: str = cammy["cammy_ssfn"]
        self.skip_email: bool = cammy["skip_email"]
        self.parent: QMainWindow = ui

    def run(self) -> None:
        if not self.file_path.steam_install_state:
            # 如果没有安装steam,则提示
            self.msg.emit("请先安装steam")
        else:
            try:
                self.__kill_steam()
                self.__determine_login_method()
                self.__download_ssfn()
                logger.info(f"账号: {self.user} 密码: {self.pwd} SSFN: {self.ssfn} 正在登录")
                logger.info(
                    f"登录参数：{self.file_path.steam_exe_path} -Windowed -login {self.user} {self.pwd}"
                )
                self.__login()
            except Exception as e:
                logger.error(f"登录失败:\n {e}")

    def __login(self) -> None:
        """登录Steam"""
        try:
            subprocess.run(
                f"{self.file_path.steam_exe_path} -Windowed -noreactlogin -login {self.user} {self.pwd}",
                cwd=self.file_path.steam_path,
            )
        except FileNotFoundError as e:
            self.login_state.emit(
                False, f"Steam路径错误,请检查\n当前启动路径:{self.file_path.steam_exe_path}"
            )
        except PermissionError:
            self.login_state.emit(
                False, "上号器无权访问Steam\n请检查: \n - 杀软是否关闭\n - Steam.exe所在文件夹权限"
            )
        except Exception as e:
            self.login_state.emit(False, f"{e}")

    @staticmethod
    def __kill_steam() -> None:
        """结束steam进程"""
        # 遍历所有进程
        for proc in psutil.process_iter():
            try:
                # 判断进程是否为Steam, 如果是就直接结束
                proc.kill() if proc.name() == "steam.exe" else None
            except Exception as e:
                logger.error(e)

    def __download_ssfn(self) -> None:
        """
        下载SSFN
        :return:
        """
        if self.ssfn:
            self.file_path.remove_ssfn()  # 删除SSFN
            with open(Path(self.file_path.steam_path) / self.ssfn, "wb") as f:
                f.write(
                    requests.get(f"http://1.15.97.14:8848/ssfn/{self.ssfn}").content
                )

    def __determine_login_method(self) -> None:
        # 判断登录模式
        if self.skip_email:
            key_value = 4
        else:
            key_value = 0
        # 打开注册表键
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS
        )
        winreg.SetValueEx(key, "StartupMode", 0, winreg.REG_DWORD, key_value)  # 修改键值
        winreg.CloseKey(key)  # 关闭注册表键
        logger.info(f"已修改 StartupMode 为： {key_value}")
