#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-7-1 下午 08:37
# @Author :Qiao

from abc import ABC

from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo


class BaseConfig:
    def __init__(self) -> None:
        self.createTemplate()

    def createTemplate(self) -> None:
        self.AccountDataListTemplate = []
        self.AccountDataDictTemplate = {  # 文件模板
            "cammy_user": "",
            "cammy_pwd": "",
            "cammy_ssfn": "",
            "Timestamp": "",
            "skip_email": False,
        }
        self.ConfigTemplate = {  # 通用设置
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
                "ping_time": 0.5,
            },
            "steam_set": {"path": None},
        }


class BaseConfigClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Config", "BaseConfig"),)

    # 静态方法available()，用于检查模块"Config"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Config")

    # 静态方法create()，用于创建BaseConfig类的实例，返回值为BaseConfig对象。
    @staticmethod
    def create(create_type: [BaseConfig]) -> BaseConfig:
        return BaseConfig()


add_creator(BaseConfigClassCreator)
