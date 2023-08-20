#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :SteamAPI.py
# @Time :2023-8-19 下午 02:16
# @Author :Qiao
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from requests.exceptions import RequestException

from Core.share.ErrorHandling import RequestExceptionErrorDispose


class SteamAPi(QThread):
    """SteamAPI相关的功能"""

    userSummarySignal = pyqtSignal(bool, dict)

    BASE_URL = "https://api.qiao.icu/SteamApi"
    GET_PLAYER_SUMMARIES = f"{BASE_URL}/GetPlayerSummaries?steam_id="

    userSummaryDIct = {
        "userProfileUrl": None,
        "userAvatar": None,
        "userAvatarHash": None,
    }

    def __init__(self, steamID: int, parentClass):
        super().__init__(parent=parentClass)
        self.steamID = steamID
        self.parentClass = parentClass

    def run(self) -> None:
        self.getPlayerSummaries()

    def getPlayerSummaries(self):
        """获取用户数据"""
        url = f"{self.GET_PLAYER_SUMMARIES}{self.steamID}"
        try:
            self.userSummary = requests.get(url).json()["response"]["players"]
            if bool(self.userSummary):
                # 如果返回的值为空
                self.userSummary = self.userSummary[0]
                self.userSummaryDIct["userProfileUrl"] = self.userSummary["profileurl"]
                self.userSummaryDIct["userAvatar"] = self.userSummary["avatarfull"]
                self.userSummaryDIct["userAvatarHash"] = self.userSummary["avatarhash"]
                self.userSummarySignal.emit(True, self.userSummaryDIct)
            else:
                self.userSummarySignal.emit(False, self.userSummaryDIct)
        except RequestException as errorMsg:
            # 无法遇测的错误
            self.userSummarySignal.emit(False, self.userSummaryDIct)
            RequestExceptionErrorDispose(self.parentClass, errorMsg)


if __name__ == "__main__":
    api = SteamAPi(76561199057860917, None)
    print(api.getPlayerSummaries())
