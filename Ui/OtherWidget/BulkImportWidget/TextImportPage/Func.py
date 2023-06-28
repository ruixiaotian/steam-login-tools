from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
)
from creart import create

from core.event_animation.other_page.bulk_page import TextImportPageAnimation


class FilePathFunc:
    def __init__(self):
        from Ui.OtherWidget.BulkImportWidget.TextImportPage import TextImportPage

        self.card_wgt = create(TextImportPage).widget
        self.file_path_edit = create(TextImportPage).file_path_edit
        self.date_func_control_list = create(TextImportPage).date_func_control_list
        self.font = create(TextImportPage).font

    def chose_file_path_trough(self) -> None:
        """选择文件按钮绑定槽函数"""
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self.card_wgt,
            caption="打开账号数据",
            directory=str(Path.home() / "Desktop"),
            filter="Text Files (*.txt)",
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
                    create(TextImportPageAnimation).table_exit_move(),
                    self.file_path_edit.removeAction(action),
                )
            )
            # 添加Action
            self.file_path_edit.addAction(action, QLineEdit.TrailingPosition)


class DataParsingFunc:
    """数据解析控件功能"""

    def __init__(self):
        from Ui.OtherWidget.BulkImportWidget.TextImportPage import TextImportPage
        from Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard import (
            TextImportTabelCard,
        )

        self.card_wgt = create(TextImportTabelCard).widget
        self.table_wgt = create(TextImportTabelCard).data_table
        self.file_path = create(TextImportPage).file_path_edit.text()
        self.separator = create(TextImportPage).separator_edit.text()
        self.encode = create(TextImportPage).encod_edit.text()
        self.count_label = create(TextImportTabelCard).count_label
        self.import_btn = create(TextImportTabelCard).import_button
        self.font = create(TextImportPage).font

    def parse_button_trough(self):
        """解析数据槽函数"""
        # 解析数据
        data_list = [["无数据"]] if not self.data_parse() else self.data_parse()
        self.table_wgt.setRowCount(0)  # 清理
        self.count_label.setText(f"共计找到 {len(data_list).__str__()} 组数据")
        for data in data_list:
            row = self.table_wgt.rowCount()  # 获取行
            self.table_wgt.insertRow(row)  # 插入行
            self.table_wgt.setRowHeight(row, 15)
            for num, d in enumerate(data):
                item = QTableWidgetItem(d)  # 创建项
                item.setToolTip(d)
                item.setFont(QFont(self.font, 8))  # 设置项字体
                item.setTextAlignment(Qt.AlignVCenter)
                self.table_wgt.setItem(row, num, item)  # 插入项

        # 显示数据
        create(TextImportPageAnimation).table_enter_move()

    def data_parse(self) -> list:
        """数据解析"""
        try:
            with open(Path(self.file_path), "r", encoding=self.encode) as f:
                return [
                    data.split(self.separator, 3)
                    for data in [data.strip() for data in f.readlines()]
                ]

        except FileNotFoundError:
            QMessageBox.critical(self.card_wgt, "打开TXT文件时出错", "文件不存在", QMessageBox.Ok)

        except UnicodeError:
            QMessageBox.critical(self.card_wgt, "打开TXT文件时出错", "文件编码错误", QMessageBox.Ok)

        except PermissionError:
            QMessageBox.critical(self.card_wgt, "打开TXT文件时出错", "权限不足", QMessageBox.Ok)

        except Exception as e:
            QMessageBox.critical(
                self.card_wgt, "打开TXT文件时出错", f"未知错误:{e}", QMessageBox.Ok
            )
