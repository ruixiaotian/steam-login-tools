#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :createCard.py
# @Time :2023-7-11 上午 11:27
# @Author :Qiao
from pathlib import Path

from abc import ABC
from creart import add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.SettingWidget.Card.CardBase import CardBase


class CommonCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/common_settings.svg")
        self.text_content = "通用设置"
        self.baseInitialize()


class LoginCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/login_settings.svg")
        self.text_content = "登录设置"
        self.baseInitialize()


class AuthorizationCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/authorization_settings.svg")
        self.text_content = "授权设置"
        self.baseInitialize()


class AboutCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/about.svg")
        self.text_content = "关于软件"
        self.baseInitialize()


class QQCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/qq.svg")
        self.text_content = "交流反馈"
        self.baseInitialize()


class AddCard(CardBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self, font: str) -> None:
        self.font = font
        self.icon_path = Path("./img/SettingWidget/Card/add.svg")
        self.text_content = "敬请期待"
        self.baseInitialize()


class CommonCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "CommonCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建CommonCard类的实例，返回值为CommonCard对象。
    @staticmethod
    def create(create_type: [CommonCard]) -> CommonCard:
        return CommonCard()


class LoginCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "LoginCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建LoginCard类的实例，返回值为LoginCard对象。
    @staticmethod
    def create(create_type: [LoginCard]) -> LoginCard:
        return LoginCard()


class AuthorizationCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "AuthorizationCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建AuthorizationCard类的实例，返回值为AuthorizationCard对象。
    @staticmethod
    def create(create_type: [AuthorizationCard]) -> AuthorizationCard:
        return AuthorizationCard()


class AboutCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "AboutCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建AboutCard类的实例，返回值为AboutCard对象。
    @staticmethod
    def create(create_type: [AboutCard]) -> AboutCard:
        return AboutCard()


class QQCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "QQCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建QQCard类的实例，返回值为QQCard对象。
    @staticmethod
    def create(create_type: [QQCard]) -> QQCard:
        return QQCard()


class AddCardClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.SettingWidget.Card.createCard", "AddCard"),)

    # 静态方法available()，用于检查模块"Ui.SettingWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.SettingWidget.Card.createCard")

    # 静态方法create()，用于创建AddCard类的实例，返回值为AddCard对象。
    @staticmethod
    def create(create_type: [AddCard]) -> AddCard:
        return AddCard()


add_creator(CommonCardClassCreator)
add_creator(LoginCardClassCreator)
add_creator(AuthorizationCardClassCreator)
add_creator(AboutCardClassCreator)
add_creator(QQCardClassCreator)
add_creator(AddCardClassCreator)
