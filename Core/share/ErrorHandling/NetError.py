#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :NetError.py
# @Time :2023-8-19 下午 08:09
# @Author :Qiao
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from qfluentwidgets.components import MessageBox

from Core.config import FEEDBACK_URL


class RequestExceptionErrorDispose:
    """Request库中无法预测的错误"""

    def __init__(self, errorMsg, parentClass) -> None:
        self.errorMsg = errorMsg
        self.parentClass = parentClass
        self.__setupMsg()
        self.box.exec()

    def __setupMsg(self):
        """设置弹窗"""
        title = self.parentClass.tr("NetWork Error")
        content = self.parentClass.tr(
            "When we requested a network resource, "
            "an unknown error occurred, "
            "and the error message caught is as follows:\n"
            f"{self.errorMsg}"
        )

        self.box = MessageBox(title, content, self.parentClass)
        self.box.yesButton.setText(self.parentClass.tr("Submit to issues!"))
        self.box.cancelButton.setText(self.parentClass.tr("OK!"))
        self.box.yesSignal.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
