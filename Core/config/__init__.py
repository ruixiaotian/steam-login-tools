#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :__init__.py.py
# @Time :2023-8-17 下午 11:32
# @Author :Qiao

from enum import Enum

from PyQt5.QtCore import QLocale
from creart import create
from qfluentwidgets.common import (
    Theme,
    qconfig,
    QConfig,
    ColorConfigItem,
    EnumSerializer,
    OptionsConfigItem,
    OptionsValidator,
    ConfigSerializer,
)

from Core.FileFunction import JsonFunc


class Language(Enum):
    """语言枚举"""

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """语言序列化"""

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Config(QConfig):
    """配置程序"""

    # 个性化
    themeMode = OptionsConfigItem(
        group="Personalize",
        name="ThemeMode",
        default=Theme.AUTO,
        validator=OptionsValidator(Theme),
        serializer=EnumSerializer(Theme),
    )
    themeColor = ColorConfigItem(
        group="Personalize", name="ThemeColor", default="#009faa"
    )
    language = OptionsConfigItem(
        group="Personalize",
        name="Language",
        default=Language.AUTO,
        validator=OptionsValidator(Language),
        serializer=LanguageSerializer(),
        restart=True
    )


HELP_URL = "https://github.com/ruixiaotian/steam-login-tools#readme"
REPO_URL = "https://github.com/ruixiaotian/steam-login-tools"
QQ_GROUP_URL = "https://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=HKLOkGuFAwy0gn73C55Ihfoyl_GOozsx&authKey=VJemhTt63V1nbBqk%2BtvuqGLSLF9kxePs4CL1ffZxTp2sRPFBPBNkLcznR3TSVmLw&noverify=0&group_code=979729394"
FEEDBACK_URL = "https://github.com/ruixiaotian/steam-login-tools/issues"

cfg = Config()
qconfig.load(create(JsonFunc).config_path, cfg)
