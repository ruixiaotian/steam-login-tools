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
from pathlib import Path
from json.decoder import JSONDecodeError


class FileOperation:
    """文件各类文件操作"""

    __config = []

    template = {  # 文件模板
        'cammy_user': '',
        'cammy_pwd': '',
        'cammy_ssfn': '',
        'steam64_id': '',
        'AccountName': '',
        'WantsOfflineMode': '',
        'MostRecent': '',
        'Timestamp': '',
        'first_login': True,
        'img_path': './img/icon/icon.ico',
        'login_method': 1
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

    def __get_steam_path(self):
        try:
            # 打开Steam注册表键
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam")
            # 读取Steam安装路径的值
            value = winreg.QueryValueEx(key, "SteamPath")
            # 赋值Steam安装路径
            # Steam根目录
            self.steam_path = Path(value[0])
            self.steam_exe_path = self.steam_path / 'steam.exe'
            # Steam用户文件目录
            self.__steam_config_path = self.steam_path / 'config'
            self.steam_user_path = self.__steam_config_path / 'loginusers.vdf'
            self.steam64id_path = self.__steam_config_path / 'config.vdf'
            # Steam图片目录
            self.steam_avatarcache_path = self.steam_path / 'avatarcache'

            # 设置安装状态
            self.steam_install_state = True
        except Exception as e:
            # 设置安装状态
            self.steam_install_state = False
            print(e)

    def __init_file(self):
        """判断文件是否存在,不存在则创建"""
        # 程序目录判断
        self.ridge_club_path.mkdir(exist_ok=True)
        self.login_data_path.mkdir(exist_ok=True)
        # 卡密数据json创建
        if not self.cammy_data_path.exists():
            # 如果文件不存在就创建
            with open(self.cammy_data_path, 'w', encoding='utf-8') as f:
                # 编码为utf-8, 否则会报错, 会导致json解析失败, 所以需要使用ensure_ascii=False
                json.dump(self.__config, f, ensure_ascii=False, indent=4)

    def read_json(self) -> list:
        """读取json文件"""
        try:
            with open(self.cammy_data_path, 'r', encoding='utf-8') as f:
                # 编码为utf-8, 否则会报错, 会导致json解析失败, 所以需要使用ensure_ascii=False
                return json.load(f)
        except JSONDecodeError as e:
            return e

    def write_json(self, data):
        """写入json文件"""
        with open(self.cammy_data_path, 'w', encoding='utf-8') as f:
            # 编码为utf-8, 否则会报错, 会导致json解析失败, 所以需要使用ensure_ascii=False
            json.dump(data, f, ensure_ascii=False, indent=4)

    def modify_json(self, data: dict | int, insert: bool = False, add: bool = False, remove: bool = False):
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
            config = self.read_json()  # 读取json文件
            config.insert(data.keys()[0], data.values()[0])  # 插入数据
            self.write_json(config)  # 写入入json文件
        if add and type(data) == dict:
            config = self.read_json()  # 读取json文件
            config.append(data)  # 加入数据
            self.write_json(config)  # 写入入json文件
        if remove and type(data) == int:
            config = self.read_json()  # 读取json文件
            config.pop(data)  # 删除数据
            self.write_json(config)  # 写入入json文件

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

        if config['users'][steam64id]['WantsOfflineMode'] == 0:
            # 判断是否需要更改
            return
        else:
            config['users'][steam64id]['WantsOfflineMode'] = 1
            config['users'][steam64id]['SkipOfflineModeWarning'] = 1
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

        if config['users'][steam64id]['WantsOfflineMode'] == 0:
            # 判断是否需要更改
            return
        else:
            config['users'][steam64id]['WantsOfflineMode'] = 0
            config['users'][steam64id]['SkipOfflineModeWarning'] = 0
            with open(file_path, 'w', encoding='utf-8') as f:
                vdf.dump(config, f, pretty=True)


if __name__ == '__main__':
    f = FileOperation()
    f.remove_ssfn()
