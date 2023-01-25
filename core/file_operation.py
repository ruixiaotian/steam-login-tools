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
from pathlib import Path
from json.decoder import JSONDecodeError


class FileOperation:
    """文件各类文件操作"""

    def __init__(self):
        """初始化对象"""
        self.document_path = Path(winreg.QueryValueEx(
            winreg.OpenKeyEx(
                winreg.HKEY_CURRENT_USER,  # 传入Key
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"  # 获取主要路径
            ), 'Personal'  # 传入Key
        )[0]
                                  )
        self.ridge_club_path = self.document_path / 'Bridge Club'
        self.login_data_path = self.ridge_club_path / 'steam_login_data'
        self.cammy_data_path = self.login_data_path / 'cammy.json'
        self.init_file()

    def init_file(self):
        """判断文件是否存在,不存在则创建"""
        self.ridge_club_path.mkdir(exist_ok=True)
        self.login_data_path.mkdir(exist_ok=True)
        if not self.cammy_data_path.exists():
            config = {
                '0': {
                    'cammy_user': '',
                    'cammy_pwd': '',
                    'cammy_ssfn': '',
                    'steam64_id': '',
                    'AccountName': '',
                    'PersonaName': '',
                    'WantsOfflineMode': '',
                    'SkipOfflineModeWarning': '',
                    'MostRecent': '',
                    'Timestamp': '',
                }
            }
            with open(self.cammy_data_path, 'w', encoding='utf-8') as file:
                json.dump(config, file)

    def del_json_found(self) -> bool:
        """删除原json重新创建

        :return: bool
        """
        if self.cammy_data_path.exists():
            self.cammy_data_path.unlink()
        self.init_file()

    def read_json_file(self) -> dict:
        """读取json文件并返回

        :return: dict
        """
        with open(self.cammy_data_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_json_file(self, json_data: dict) -> bool:
        """写入JSON文件
        :param json_data 写入的数据
        :return: bool
        """
        with open(self.cammy_data_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file)
        return True

    def json_is_empty(self) -> bool:
        """判断Json是否为空或者为初始化创建的

        :return: bool
        """
        try:
            with open(self.cammy_data_path, 'r', encoding='utf-8') as file:
                print(json.load(file)['0'])
            return True
        except NameError:
            self.del_json_found()
            return False
        except JSONDecodeError:
            self.del_json_found()
            return False
        except KeyError:
            self.del_json_found()
            return False


if __name__ == '__main__':
    f = FileOperation()
