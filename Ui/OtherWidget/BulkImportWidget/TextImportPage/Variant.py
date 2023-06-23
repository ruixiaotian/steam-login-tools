from abc import ABC
from pathlib import Path

from PyQt5.QtWidgets import QLineEdit, QWidget, QFileDialog, QAction
from PyQt5.QtGui import QIcon
from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from core.event_animation.other_page.bulk_page import text_wgt_max_size, text_wgt_min_size


class FilePathFunc:

    def chose_file_path_trough(self, parent: QWidget, file_path_edit: QLineEdit) -> None:
        """选择文件按钮绑定槽函数"""
        file_path, _ = QFileDialog.getOpenFileName(
            parent=parent, caption='打开账号数据',
            directory=str(Path.home()), filter='Text Files (*.txt)'
        )
        if not file_path:
            # 检查用户是否选择文件
            return
        else:
            # 设置编辑框内容
            file_path_edit.setText(file_path)
            # 放大卡片
            text_wgt_max_size(parent)
            # 添加Action
            self.add_clean_path(parent, file_path_edit)

    def add_clean_path(self, parent: QWidget, file_path_edit: QLineEdit) -> None:
        """添加清理路径的Action"""
        if not file_path_edit.actions():
            # 判断是否已经有Action,没有则创建
            action = QAction(
                QIcon("./img/OtherWidget/bulk/clean.svg"), "清空", file_path_edit
            )
            # 链接Action信号
            action.triggered.connect(
                lambda: (file_path_edit.clear(), text_wgt_min_size(parent), file_path_edit.removeAction(action))
            )
            # 添加Action
            file_path_edit.addAction(action, QLineEdit.TrailingPosition)
