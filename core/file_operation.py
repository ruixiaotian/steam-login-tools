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

    def write_json_file(self, json_data: dict) -> [bool, str]:
        """写入JSON文件
        :param json_data 写入的数据
        :return: [bool, str]
        """
        try:
            with open(self.cammy_data_path, 'r', encoding='utf-8') as file:
                old_json_data: dict = json.load(file)
            if self.json_is_empty():
                # 判断是否为初始化时创建的数据,如果不是则追加,如果是则覆盖
                print(json_data.values())
                old_json_data[list(json_data.keys())[0]] = list(json_data.values())[0]
            else:
                old_json_data.clear()
                print(json_data.keys())
                old_json_data[list(json_data.keys())[0]] = list(json_data.values())[0]
            with open(self.cammy_data_path, 'w', encoding='utf-8') as file:
                json.dump(old_json_data, file)
            return True
        except Exception as msg:
            print(msg)
            return False, msg

    def json_is_empty(self) -> bool:
        """判断Json是否为空或者为初始化创建的

        :return: bool
        """
        try:
            with open(self.cammy_data_path, 'r', encoding='utf-8') as file:
                json_data: dict = json.load(file)
            for i in json_data.keys():
                # 判断是否为初始化创建的数据
                if i == '0':
                    return False
                else:
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


class XmlFileOperation:
    """xml文件操作"""

    @staticmethod
    def revise_svg_color(svg_path, old_color, new_color) -> None:
        """
        该函数用于修改xml文件中的颜色
        需要传入svg文件路径，旧颜色，新颜色(需要十六进制格式)
        :param svg_path:
        :param old_color:
        :param new_color:
        :return: None
        """
        # 解析SVG文件
        with open(svg_path, 'r', encoding='utf-8') as f:  # 读入文件
            parser = etree.XMLParser(remove_blank_text=True)  # 删除掉空白文本
            svg = etree.parse(f, parser)  # 解析SVG文件

        # 修改颜色
        for element in svg.iter():  # 变例历所有元素
            if 'fill' in element.attrib:  # 判断是否包含fill属性
                element.attrib['fill'] = element.attrib['fill'].replace(old_color, new_color)  # 替换颜色

        # 保存修改后的文件
        with open(svg_path, 'wb') as f:  # 读入文件
            f.write(etree.tostring(svg, pretty_print=True))  # 写入文件


if __name__ == '__main__':
    f = FileOperation()
