from abc import ABC

from PyQt5.QtWidgets import QLineEdit, QCompleter, QWidget

import string
from pathlib import Path

from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from core.event_animation.other_page.bulk_page import text_wgt_max_size, text_wgt_min_size


class FilePathCompletion:

    def __init__(self, file_path: QLineEdit):
        """初始化对象"""
        self.edit: QLineEdit = file_path

    def path_completion(self, text: str):
        """联想文件路径"""
        if not text:
            # 如果为空则直接退出
            return

        if len(text) == 1 and text in string.ascii_letters:
            # 如果第一个字符是字母
            text = f"{text.title()}:\\"
            self.edit.setText(text)

        if text[-1] == "\\":
            # 如果最后一个字符是反斜杠
            self.edit.setCompleter(None)
            # 设置联想项
            completion_list = [path.__str__() for path in Path(text).glob("*")]
            # 设置联想器
            completion = QCompleter(completion_list, self.edit)
            completion.setCompletionMode(QCompleter.InlineCompletion)
            self.edit.setCompleter(completion)

    def file_judgement(self, txt_page: QWidget):
        # 设置文件路径
        file_path = Path(self.edit.text())

        # 判断是否为文件以及路径是否存在和后缀是否为txt
        if file_path.is_file() and file_path.exists() and file_path.suffix == ".txt":
            text_wgt_max_size(txt_page)
