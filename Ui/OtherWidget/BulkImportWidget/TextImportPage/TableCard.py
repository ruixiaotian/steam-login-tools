#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :TableCard.py
# @Time :2023-6-26 下午 10:09
# @Author :Qiao
from abc import ABC

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidget, QHeaderView, QAbstractItemView
from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.Share import shadow_setup


class TextImportTabelCard:

    def __init__(self):
        self.widget = QWidget()

    def initialize(self, font: str):
        """接收参数和初始化"""
        # 创建变量
        self.font = font

        # 初始化
        self.widget.setObjectName("author_info_widget")
        shadow_setup(self.widget, (2, 2), 10, QColor(29, 190, 245, 60))
        # 隐藏控件
        self.widget.setHidden(True)

    def table_card(self):
        """表格卡片构建"""
        # 创建大控件
        layout = QGridLayout(self.widget)

        # 创建表格子控件
        self.data_table = QTableWidget()

        # 设置控件
        self.data_table.setFixedSize(520, 315)  # 固定大小
        self.data_table.setHorizontalHeaderLabels(["数据"])  # 设置表头
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表头自适应
        self.data_table.horizontalHeader().setSectionsClickable(False)  # 禁止点击表头
        self.data_table.verticalHeader().setVisible(False)  # 隐藏行表头
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置禁止编辑
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.data_table.setWordWrap(True)
        # 设置属性名
        self.data_table.setObjectName("TextImportPageDateTable")
        # 添加到控件
        layout.addWidget(self.data_table)
        layout.setVerticalSpacing(0)

        return self.widget


class TextImportTabelCardCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard",
            "TextImportTabelCard"
        ),
    )

    # 静态方法available()，用于检查模块"TableCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard")

    # 静态方法create()，用于创建TextImportTabelCard类的实例，返回值为TextImportTabelCard对象。
    @staticmethod
    def create(create_type: [TextImportTabelCard]) -> TextImportTabelCard:
        return TextImportTabelCard()


add_creator(TextImportTabelCardCreator)



