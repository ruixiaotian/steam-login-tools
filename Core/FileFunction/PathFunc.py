#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :FileFunctionBase.py
# @Time :2023-7-22 下午 08:25
# @Author :Qiao
"""
获取程序所需的所有路径
"""
import winreg
from abc import ABC
from pathlib import Path
from typing import List

from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo


class PathFunc:
    """文件操作基类"""

    def __init__(self):
        """初始化"""
        self.base_path = self.getBasePath()
        self.exe_path = self.base_path / "steam_login_tools"
        self.data_path = self.base_path / "steam_login_data"

        self.steam_base_path = self.getSteamPath()
        self.steam_path = self.steam_base_path[0]
        self.steam_exe_path = self.steam_base_path[1]

    @staticmethod
    def getBasePath() -> Path:
        """获取软件路径"""
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
        )
        return Path(winreg.QueryValueEx(key, "Personal")[0]) / "Bridge Club"

    @staticmethod
    def getSteamPath() -> List[Path]:
        """获取Steam路径"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        return [
            Path(winreg.QueryValueEx(key, "SteamPath")[0]),
            Path(winreg.QueryValueEx(key, "SteamExe")[0]),
        ]


class PathFuncClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Core.FileFunction.PathFunc", "PathFunc"),)

    # 静态方法available()，用于检查模块"PathFunc"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Core.FileFunction.PathFunc")

    # 静态方法create()，用于创建PathFunc类的实例，返回值为PathFunc对象。
    @staticmethod
    def create(create_type: [PathFunc]) -> PathFunc:
        return PathFunc()


add_creator(PathFuncClassCreator)
