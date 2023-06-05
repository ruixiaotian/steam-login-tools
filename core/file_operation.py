#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 11:08
# @Author  : 桥话语权
# @File    : file_operation.py
# @Software: PyCharm
"""
 *  用于文件的增删改查操作
"""
import json
import winreg
import vdf
import asyncio
from loguru import logger
from pathlib import Path
from json.decoder import JSONDecodeError
from PyQt5.QtCore import QThread, pyqtSignal

from creart import create, exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo
from abc import ABC


class FileOperation:
    """文件各类文件操作"""

    __cammy = []  # 卡密模板

    __config = {  # 通用设置
        "common_set": {
            "auto_update": True,
            "boot_auto_start": False,
            "minimize_on_startup": False,
            "tray_icon": False,
        },
        "server_set": {  # 授权服务器设置
            "server1": "",
            "server1_port": "",
            "server2": "",
            "server2_port": "",
            "server3": "",
            "server3_port": "",
            "ping_info": False,
            "ping_time": 0.5
        },
        "steam_set": {
            "path": {
                "old": None,
                "new": None
            },
            "version": ""
        }
    }

    template = {  # 文件模板
        'cammy_user': '',
        'cammy_pwd': '',
        'cammy_ssfn': '',
        'steam64_id': '',
        'AccountName': '',
        'Timestamp': '',
        'WantsOfflineMode': False,
        'MostRecent': False,
        'skip_email': False,
        'img_path': './img/icon/login_widget/account_info/null_img.png',
    }

    def __init__(self):
        """初始化对象"""
        self.__get_path()
        self.__get_steam_path()
        self.__init_file()

    def __get_path(self):
        """
        获取重新需要用到的路径
        :return:
        """
        # 获取系统文档路径
        shell_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        winreg_key = winreg.HKEY_CURRENT_USER
        open_reg = winreg.OpenKeyEx(winreg_key, shell_path)
        self.document_path = Path(winreg.QueryValueEx(open_reg, 'Personal')[0])

        # 获取软件数据存放路径
        self.ridge_club_path = self.document_path / 'Bridge Club'
        self.login_data_path = self.ridge_club_path / 'steam_login_data'
        self.cammy_data_path = self.login_data_path / 'cammy.json'
        self.config_data_path = self.login_data_path / 'config.json'

    def __get_steam_path(self):
        try:
            # 初始化配置文件
            self.config_data = self.read_config_json()
            # 判断配置文件中是否存在steam路
            if self.config_data["steam_set"]["path"]["new"] is None:
                # 打开Steam注册表键
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam")
                # 读取Steam安装路径的值
                value = winreg.QueryValueEx(key, "SteamPath")
                # Steam根目录
                self.steam_path = Path(value[0])
                # 写入config文件夹
                self.config_data["steam_set"]["path"]["new"] = str(self.steam_path)
                self.config_data["steam_set"]["version"] = "new"
                self.write_json(self.config_data_path, self.config_data)

            if self.config_data["steam_set"]["version"] == "new":
                # 判断版本
                self.steam_path = Path(self.config_data["steam_set"]["path"]["new"])
            elif self.config_data["steam_set"]["version"] == "old":
                self.steam_path = Path(self.config_data["steam_set"]["path"]["old"])

            self.steam_exe_path = self.steam_path / 'steam.exe'
            # Steam用户文件目录
            self.__steam_config_path = self.steam_path / 'config'
            self.steam_user_path = self.__steam_config_path / 'loginusers.vdf'
            self.steam64id_path = self.__steam_config_path / 'config.vdf'
            # Steam图片目录
            self.steam_avatarcache_path = self.__steam_config_path / 'avatarcache'

            # 设置安装状态
            self.steam_install_state = True
            logger.info(f"监测到Steam路径:{self.steam_path}")
        except Exception as e:
            # 设置安装状态
            self.steam_install_state = False
            logger.error(f"未能获取到Steam安装路径：{e}\n")

    def __init_file(self):
        """判断文件是否存在,不存在则创建"""
        # 程序目录判断
        self.ridge_club_path.mkdir(exist_ok=True, parents=True)
        self.login_data_path.mkdir(exist_ok=True, parents=True)
        # 卡密数据json创建
        if not self.cammy_data_path.exists():  # 如果卡密文件不存在就创建
            with open(self.cammy_data_path, 'w', encoding='utf-8') as f:
                json.dump(self.__cammy, f, ensure_ascii=False, indent=4)
        if not self.config_data_path.exists():  # 如果配置文件不存在，则创建配置文件
            with open(self.config_data_path, 'w', encoding='utf-8') as f:
                json.dump(self.__config, f, ensure_ascii=False, indent=4)

    def read_cammy_json(self) -> list:
        """读取卡密json文件"""
        try:
            with open(self.cammy_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except JSONDecodeError as e:
            return e

    def read_config_json(self):
        """读取配置文件,方便外部访问"""
        try:
            with open(self.config_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except JSONDecodeError as e:
            return e

    @staticmethod
    def write_json(file_path, data):
        """写入json文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            # 编码为utf-8, 否则会报错, 会导致json解析失败, 所以需要使用ensure_ascii=False
            json.dump(data, f, ensure_ascii=False, indent=4)

    def modify_json(
            self, file_path: str | Path, data: dict | int,
            insert: bool = False, add: bool = False, remove: bool = False
    ):
        """
        修改json文件, 主要操作为插入/追加/删除某个值
        传入格式:

        insert模式:
        data : dict 传入一个字典,其key为要插入的序号,value为要插入的数据
        insert 传入 True

        add模式:
        data : dict 传入数据,直接追加到最后
        add 传入 True

        remove模式:
        data : int 传入一个数字,其为要删除的序号
        remove 传入 True
        """
        if insert and type(data) == dict:
            # 如果是插入模式
            config = self.read_cammy_json()  # 读取json文件
            config.insert(data.keys()[0], data.values()[0])  # 插入数据
            self.write_json(file_path, config)  # 写入入json文件
        if add and type(data) == dict:
            config = self.read_cammy_json()  # 读取json文件
            config.append(data)  # 加入数据
            self.write_json(file_path, config)  # 写入入json文件
        if remove and type(data) == int:
            config = self.read_cammy_json()  # 读取json文件
            config.pop(data)  # 删除数据
            self.write_json(file_path, config)  # 写入入json文件

    def remove_ssfn(self):
        """删除SSFN"""
        try:
            # 遍历文件夹中的所有文件
            for file_path in self.steam_path.glob('*'):
                # 判断是否为文件，且文件名是否以指定开头
                if file_path.is_file() and file_path.name.startswith('ssfn'):
                    # 删除文件
                    file_path.unlink()
        except Exception as e:
            print(e)


class VdfOperation:
    """Vdf文件操作"""

    @staticmethod
    def read_vdf(file_path: str) -> dict:
        """读取Vdf文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return vdf.load(f)['users']
        except Exception as e:
            return e

    @staticmethod
    def write_vdf(file_path: str, data: dict):
        """写入Vdf文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            vdf.dump(data, f, pretty=True)

    @staticmethod
    def wants_offline_mode(file_path: str, steam64id: str):
        """
        修改离线模式为True
        判断是否默认离线模式,不是则修改
        :param file_path:
        :param steam64id:
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            config = vdf.load(f)

        if config['users'][steam64id]['WantsOfflineMode'] == "0":
            # 判断是否需要更改
            return
        else:
            config['users'][steam64id]['WantsOfflineMode'] = "1"
            config['users'][steam64id]['SkipOfflineModeWarning'] = "1"
            with open(file_path, 'w', encoding='utf-8') as f:
                vdf.dump(config, f, pretty=True)

    @staticmethod
    def not_offline_mode(file_path: str, steam64id: str):
        """
        修改离线模式为False
        判断是否默认不离线模式,不是则修改
        :param file_path:
        :param steam64id:
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            config = vdf.load(f)

        if config['users'][steam64id]['WantsOfflineMode'] == "0":
            # 判断是否需要更改
            return
        else:
            config['users'][steam64id]['WantsOfflineMode'] = "0"
            config['users'][steam64id]['SkipOfflineModeWarning'] = "0"
            with open(file_path, 'w', encoding='utf-8') as f:
                vdf.dump(config, f, pretty=True)


def detect_vdf():
    """监测vdf"""
    if not create(FileOperation).steam_install_state:
        return
    cammy: list = create(FileOperation).read_cammy_json()
    vdf: dict = create(VdfOperation).read_vdf(create(FileOperation).steam_user_path)

    for vdf_key, vdf_value in vdf.items():
        # 读取所有vdf项
        for item in cammy:
            if vdf_value['AccountName'] in item['cammy_user']:
                item['steam64_id'] = vdf_key
                item['AccountName'] = vdf_value['AccountName']
                item['Timestamp'] = vdf_value['Timestamp']
                item['img_path'] = str(create(FileOperation).steam_avatarcache_path / f"{vdf_key}.png")
    create(FileOperation).write_json(create(FileOperation).cammy_data_path, cammy)


class FileOperationClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("core.file_operation", "FileOperation"),)

    # 静态方法available()，用于检查模块"core"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("core.file_operation")

    # 静态方法create()，用于创建FileOperation类的实例，返回值为FileOperation对象。
    @staticmethod
    def create(create_type: [FileOperation]) -> FileOperation:
        return FileOperation()


class VdfOperationClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("core.file_operation", "VdfOperation"),)

    # 静态方法available()，用于检查模块"core"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("core.file_operation")

    # 静态方法create()，用于创建VdfOperation类的实例，返回值为VdfOperation对象。
    @staticmethod
    def create(create_type: [VdfOperation]) -> VdfOperation:
        return VdfOperation()


add_creator(FileOperationClassCreator)
add_creator(VdfOperationClassCreator)

if __name__ == '__main__':
    f = DetectVdfThread()
    f.detect_vdf()
