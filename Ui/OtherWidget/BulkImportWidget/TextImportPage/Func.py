from abc import ABC
from pathlib import Path

from PyQt5.QtWidgets import QLineEdit, QWidget, QFileDialog, QAction, QMessageBox, \
    QTableWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from creart import exists_module, add_creator, create
from creart.creator import AbstractCreator, CreateTargetInfo

from core.event_animation.other_page.bulk_page import TextImportPageAnimation


class FilePathFunc:

    def __init__(self):
        from Ui.OtherWidget.BulkImportWidget.TextImportPage import TextImportPage
        from Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard import TextImportTabelCard
        self.card_wgt = create(TextImportPage).widget
        self.file_path_edit = create(TextImportPage).file_path_edit
        self.date_func_control_list = create(TextImportPage).date_func_control_list
        self.table_wgt = create(TextImportTabelCard).data_table
        self.font = create(TextImportPage).font

    def chose_file_path_trough(self) -> None:
        """选择文件按钮绑定槽函数"""
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self.card_wgt, caption='打开账号数据',
            directory=str(Path.home() / 'Desktop'), filter='Text Files (*.txt)'
        )
        if not file_path:
            # 检查用户是否选择文件
            return

        """文本框设置"""
        # 设置编辑框内容
        self.file_path_edit.setText(file_path)
        # 放大卡片
        create(TextImportPageAnimation).card_max_size()
        # 添加Action
        self.add_clean_path()

        """数据解析布局设置"""
        try:
            with open(Path(file_path), "r", encoding='utf-8') as f:
                data_list = f.readlines()
            if not data_list:
                data_list = ['无数据']
            for data in data_list:
                row = self.table_wgt.rowCount()  # 获取行
                self.table_wgt.insertRow(row)  # 插入行
                self.table_wgt.setRowHeight(row, 15)
                item = QTableWidgetItem(data)  # 创建项
                item.setToolTip(data)
                item.setFont(QFont(self.font, 8))  # 设置项字体
                item.setTextAlignment(Qt.AlignVCenter)
                self.table_wgt.setItem(row, 0, item)  # 插入项

        except UnicodeError:
            QMessageBox.critical(self.card_wgt, "打开TXT文件时出错", "文件编码错误", QMessageBox.Ok)

    def add_clean_path(self) -> None:
        """添加清理路径的Action"""
        if not self.file_path_edit.actions():
            # 判断是否已经有Action,没有则创建
            action = QAction(
                QIcon("./img/OtherWidget/bulk/clean.svg"), "清空", self.file_path_edit
            )
            # 链接Action信号
            action.triggered.connect(
                lambda: (
                    self.file_path_edit.clear(),
                    create(TextImportPageAnimation).card_min_size(),
                    self.file_path_edit.removeAction(action)
                )
            )
            # 添加Action
            self.file_path_edit.addAction(action, QLineEdit.TrailingPosition)


class DataParsingFunc:
    """数据解析控件功能"""

    def __init__(self):
        pass
