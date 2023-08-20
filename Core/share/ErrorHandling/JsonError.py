#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :JsonError.py
# @Time :2023-8-18 下午 11:14
# @Author :Qiao
import itertools
import random
import shutil
import string
from pathlib import Path

from PyQt5.QtCore import Qt
from creart import create
from qfluentwidgets.components import InfoBar, MessageBox, InfoBarPosition

from Core.FileFunction import PathFunc, JsonFunc


class JsonDecodingErrorDispose:
    """json解码错误处理"""

    def __init__(self, path: Path, parent, parentClass) -> None:
        self.path = path
        self.parent = parent
        self.parentClass = parentClass
        self.__setupMsg()
        self.box.exec()

    def __setupMsg(self) -> None:
        """设置弹窗"""
        title = self.parentClass.tr("Decode Error")
        content = self.parentClass.tr(
            "Save failed, configuration file decoding failed.  "
            "Do you want to delete the configuration file?"
            " (Please ensure that your data has been backed up) "
        )

        self.box = MessageBox(title, content, self.parentClass)
        self.box.yesButton.setText(self.parentClass.tr("delete!"))
        self.box.cancelButton.setText(self.parentClass.tr("Help me backup and delete"))

        self.box.yesSignal.connect(self.__deleteFile)
        self.box.cancelSignal.connect(self.__deleteAfterBackup)

    def __deleteFile(self) -> None:
        """直接删除文件"""
        # 删除文件并重新创建
        self.path.unlink()
        create(JsonFunc).checkDataFile()
        # 弹出消息条
        self.__delMsg()

    def __deleteAfterBackup(self) -> None:
        """备份后删除文件"""
        if not Path(create(PathFunc).desktop_path / self.path.name).exists():
            # 如果目标路径不存在,则直接移动
            shutil.move(self.path, create(PathFunc).desktop_path)
        else:
            # 如果存在,则修改一下文件名再移动
            shutil.move(self.path, self.__generateNewName())
        # 调用该方法重新创建文件
        create(JsonFunc).checkDataFile()
        # 弹出消息条
        self.__backUpDelMsg()

    def __generateNewName(self) -> Path:
        """用于生成新的文件名"""
        for count in itertools.islice(itertools.count(1), 1000):
            # 利用itertools来迭代计数
            fileName = f"{self.path.stem}({count}){self.path.suffix}"
            filePath = create(PathFunc).desktop_path / fileName
            if not filePath.exists():
                # 如果不存在了,则返回新名字
                return filePath
        else:
            # 如果上方方法不管用,则生成随机名字
            fileName = "".join(random.sample(string.ascii_letters, 16))
            fileName = f"{fileName}{self.path.suffix}"
            filePath = create(PathFunc).desktop_path / fileName
            if not filePath.exists():
                return filePath

    def __backUpDelMsg(self) -> None:
        """备份并删除成功的消息条"""
        InfoBar.success(
            title=self.parentClass.tr("Successful"),
            content=self.parentClass.tr(
                f"Successfully backed up files to: "
                f"{create(PathFunc).desktop_path / self.path.name}"
            ),
            orient=Qt.Vertical,
            isClosable=False,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self.parentClass,
        )

    def __delMsg(self):
        """删除成功消息条"""
        InfoBar.success(
            title=self.parentClass.tr("Successful"),
            content=self.parentClass.tr("The file was deleted successfully"),
            orient=Qt.Vertical,
            isClosable=False,
            position=InfoBarPosition.TOP_RIGHT,
            duration=3000,
            parent=self.parentClass,
        )
