#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @FileName :TableCard.py
# @Time :2023-6-26 下午 10:09
# @Author :Qiao
from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QWidget,
)
from creart import add_creator, create, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Config import BaseConfig
from Core.FileOperation import FileOperation
from Ui.Share import shadow_setup


class TextImportTabelCard:
    def __init__(self) -> None:
        self.widget = QWidget()
        self.data_table = QTableWidget(0, 3)
        self.count_label = QLabel()
        self.clear_button = QPushButton("清空")
        self.import_button = QPushButton("导入")

    def initialize(self, font: str) -> None:
        """接收参数和初始化"""
        # 创建变量
        self.font = font
        # 隐藏控件
        self.widget.setHidden(True)

    def table_page(self) -> QWidget:
        """表格数据控件"""
        # 创建大控件
        layout = QGridLayout(self.widget)

        """创建子控件"""
        title_wgt = self.title_control()
        table_wgt = self.table_card()

        """添加到控件"""
        layout.addWidget(title_wgt, 0, 0, 1, 1)
        layout.addWidget(table_wgt, 1, 0, 1, 1)
        layout.setVerticalSpacing(0)

        return self.widget

    def title_control(self) -> QWidget:
        """标题控件"""
        # 创建控件
        title_wgt = QWidget()
        title_layout = QGridLayout(title_wgt)
        # 创建子控件
        self.title = QLabel("数据列表")
        self.title.setFont(QFont(self.font, 10))
        self.title.setFixedHeight(13)
        self.title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.title.setObjectName("other_page_min_title_label")
        # 添加到布局
        title_layout.addWidget(self.title)
        title_layout.setContentsMargins(30, 0, 0, 0)
        title_layout.setVerticalSpacing(0)

        return title_wgt

    def table_card(self) -> QWidget:
        """表格卡片构建"""
        # 创建大控件
        card_wgt = QWidget()
        layout = QGridLayout(card_wgt)
        # 设置最大高度和对象名称
        card_wgt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        card_wgt.setObjectName("card_widget")

        # 添加到控件
        layout.addLayout(self.table_show(), 0, 0, 1, 1, Qt.AlignTop)
        layout.addLayout(self.table_func(), 1, 0, 1, 1, Qt.AlignTop)

        # 添加阴影
        shadow_setup(card_wgt, (2, 2), 10, QColor(29, 190, 245, 60))

        return card_wgt

    def table_show(self) -> QGridLayout:
        """表格展示"""
        # 创建布局
        layout = QGridLayout()

        # 设置控件
        self.data_table.setFont(QFont(self.font))
        self.data_table.setFixedHeight(200)  # 固定大小
        self.data_table.setHorizontalHeaderLabels(["账号", "密码", "SSFN"])  # 设置表头
        self.data_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # 设置表头自适应
        self.data_table.horizontalHeader().setSectionsClickable(False)  # 禁止点击表头
        self.data_table.verticalHeader().setVisible(False)  # 隐藏行表头
        self.data_table.setShowGrid(False)  # 隐藏分割线
        self.data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用垂直进度条
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置禁止编辑
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.data_table.setWordWrap(True)
        # 设置属性名
        self.data_table.setObjectName("TextImportPageDateTable")

        layout.setContentsMargins(7, 10, 1, 4)

        # 添加到控件
        layout.addWidget(self.data_table, 0, 0, 1, 1, Qt.AlignVCenter)

        return layout

    def table_func(self) -> QGridLayout:
        """表格功能"""
        # 创建布局
        layout = QGridLayout()

        # 创建控件列表
        control_list = [self.count_label, self.clear_button, self.import_button]
        control_name_list = ["count_label", "clear_button", "import_button"]

        # 设置通用属性
        _ = [control.setFont(QFont(self.font)) for control in control_list]
        _ = [
            control.setObjectName(name)
            for control, name in zip(control_list, control_name_list)
        ]
        _ = [
            shadow_setup(btn, (1, 1), 5, QColor(29, 190, 245, 40))
            for btn in [self.clear_button, self.import_button]
        ]
        _ = [
            btn.setFixedSize(65, 20) for btn in [self.clear_button, self.import_button]
        ]

        # 单独设置属性
        self.count_label.setFixedWidth(320)

        # 链接信号
        self.clear_button.clicked.connect(
            lambda: (
                self.data_table.setRowCount(0),
                self.count_label.setText("已清空所有数据"),
            )
        )
        self.import_button.clicked.connect(lambda: self.import_data())

        # 添加到布局
        layout.addWidget(self.count_label, 0, 0, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.clear_button, 0, 2, 1, 1, Qt.AlignRight)
        layout.addWidget(self.import_button, 0, 3, 1, 1, Qt.AlignRight)

        layout.setContentsMargins(15, 0, 15, 0)
        layout.setHorizontalSpacing(0)

        return layout

    def import_data(self) -> None:
        """导入卡密文件"""
        exist_data = [i["cammy_user"] for i in create(FileOperation).read_cammy_json()]
        num_duplicates = 0
        for row in range(self.data_table.rowCount()):
            # 循环导入
            if self.data_table.item(row, 0).text() in exist_data:
                # 去除重复
                num_duplicates += 1
                continue
            cammy = create(BaseConfig).AccountDataDictTemplate
            cammy["cammy_user"] = self.data_table.item(row, 0).text()
            cammy["cammy_pwd"] = self.data_table.item(row, 1).text()
            cammy["cammy_ssfn"] = self.data_table.item(row, 2).text()
            create(FileOperation).modify_json(
                create(FileOperation).cammy_data_path, cammy, add=True
            )
        self.count_label.setText(
            f"成功导入 {self.data_table.rowCount() - num_duplicates} 组数据 "
            f"去除重复 {num_duplicates} 组"
        )
        self.data_table.setRowCount(0)  # 清除列表
        from Ui.LoginWidget import LoginWidget

        create(LoginWidget).refresh_widget()  # 刷新


class TextImportTabelCardCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard",
            "TextImportTabelCard",
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
