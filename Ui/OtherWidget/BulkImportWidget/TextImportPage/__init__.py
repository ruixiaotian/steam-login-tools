from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QSizePolicy, QPushButton, \
    QTableWidget, QHeaderView, QAbstractItemView
from creart import exists_module, add_creator
from creart.creator import AbstractCreator, CreateTargetInfo

from Ui.OtherWidget.BulkImportWidget.TextImportPage.Func import FilePathFunc
from Ui.Share import shadow_setup


class TextImportPage:

    def __init__(self):
        """初始化方法"""
        self.widget = QWidget()

    def initialize(self, font: str):
        """接收参数"""
        self.font = font

    def txt_page(self) -> QWidget:
        """
        修复错误介绍控件
        :return:
        """
        # 创建大控件
        layout = QGridLayout(self.widget)

        """创建子控件"""
        title_wgt = self.title_control()
        txt_wgt = self.card_control()

        """添加到控件"""
        layout.addWidget(title_wgt, 0, 0, 1, 1)
        layout.addWidget(txt_wgt, 1, 0, 1, 1)
        layout.setVerticalSpacing(0)

        return self.widget

    def title_control(self):
        """标题控件"""
        # 创建控件
        title_wgt = QWidget()
        title_layout = QGridLayout(title_wgt)
        # 创建子控件
        self.title = QLabel("从TXT导入")
        self.title.setFont(QFont(self.font, 10))
        self.title.setFixedHeight(10)
        self.title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.title.setObjectName("other_page_min_title_label")
        # 添加到布局
        title_layout.addWidget(self.title)
        title_layout.setContentsMargins(30, 0, 0, 0)
        title_layout.setVerticalSpacing(0)

        return title_wgt

    def card_control(self):
        """卡片控件"""
        # 创建卡片控件，并设置属性
        card_wgt = QWidget()
        txt_layout = QGridLayout(card_wgt)
        # 设置最大高度
        card_wgt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置对象名称，用于QSS定位
        card_wgt.setObjectName("author_info_widget")

        # 添加到控件
        txt_layout.addLayout(self.file_choose(), 0, 0, 1, 1, Qt.AlignTop)
        txt_layout.addLayout(self.data_func(), 1, 0, 1, 1, Qt.AlignTop)
        # txt_layout.setContentsMargins(3, 0, 0, 0)

        # txt_layout.setVerticalSpacing(2)

        # 添加阴影
        shadow_setup(card_wgt, (2, 2), 10, QColor(29, 190, 245, 60))

        return card_wgt

    def file_choose(self) -> QGridLayout:
        """
        txt导入,文件选择项
        :return: QGridLayout
        """
        # 创建布局
        layout = QGridLayout()

        # 创建控件
        file_label = QLabel("文件路径:")
        self.file_path_edit = QLineEdit()
        self.file_choose_btn = QPushButton("选择文件")

        # 添加到列表
        obj_list = [file_label, self.file_path_edit, self.file_choose_btn]
        obj_name = ["file_label", "file_path_edit", "file_choose_btn"]

        # 设置属性
        _ = [obj.setFont(QFont(self.font)) for obj in obj_list]
        _ = [obj.setObjectName(name) for obj, name in zip(obj_list, obj_name)]

        # 设置控件属性
        self.file_path_edit.setTextMargins(2, 1, 1, 2)
        # 设置文本占位文字
        self.file_path_edit.setPlaceholderText("请选择文件路径")
        # 设置只读
        self.file_path_edit.setReadOnly(True)

        # 链接按钮槽函数
        self.file_choose_btn.clicked.connect(
            lambda: FilePathFunc().chose_file_path_trough()
        )

        # 设置按钮属性
        self.file_choose_btn.setFixedSize(65, 20)
        shadow_setup(self.file_choose_btn, (1, 1), 5, QColor(29, 190, 245, 40))

        # 添加到布局
        layout.addWidget(file_label, 0, 0, 1, 1, Qt.AlignVCenter)
        layout.addWidget(self.file_path_edit, 0, 1, 1, 1, Qt.AlignVCenter)
        layout.addWidget(self.file_choose_btn, 0, 2, 1, 1, Qt.AlignVCenter)

        layout.setContentsMargins(20, 10, 20, 0)
        layout.setHorizontalSpacing(8)

        return layout

    def data_func(self) -> QGridLayout:
        """操作数据控件"""
        # 创建布局
        layout = QGridLayout()

        # 创建控件
        separator_label = QLabel("分隔符:")
        self.separator_edit = QLineEdit()
        encode_label = QLabel("文件编码:")
        self.encod_edit = QLineEdit()
        self.parse_button = QPushButton("解析数据")

        # 添加到控件列表
        self.date_func_control_list = [separator_label, self.separator_edit, encode_label, self.encod_edit, self.parse_button]
        control_objname_list = ["separator_label", "separator_edit", "encode_label", "encod_edit", "parse_button"]

        # 设置通用属性
        _ = [control.setFont(QFont(self.font)) for control in self.date_func_control_list]
        _ = [control.setObjectName(name) for control, name in zip(self.date_func_control_list, control_objname_list)]

        # 设置单独属性
        separator_label.setFixedWidth(39)
        encode_label.setFixedWidth(55)
        self.separator_edit.setFixedWidth(150)
        self.encod_edit.setFixedWidth(150)

        self.separator_edit.setText("----")
        self.encod_edit.setText("utf-8")

        self.parse_button.setFixedSize(65, 20)
        shadow_setup(self.parse_button, (1, 1), 5, QColor(29, 190, 245, 40))

        # 隐藏控件
        _ = [control.setHidden(True) for control in self.date_func_control_list]

        # 添加到布局
        _ = [layout.addWidget(i, 0, num, 1, 1) for num, i in enumerate(self.date_func_control_list)]

        layout.setContentsMargins(20, 0, 20, 0)

        return layout

class TextImportPageClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Ui.OtherWidget.BulkImportWidget.TextImportPage",
            "TextImportPage"
        ),
    )

    # 静态方法available()，用于检查模块"TableCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.OtherWidget.BulkImportWidget.TextImportPage")

    # 静态方法create()，用于创建TextImportPage类的实例，返回值为TextImportPage对象。
    @staticmethod
    def create(create_type: [TextImportPage]) -> TextImportPage:
        return TextImportPage()


add_creator(TextImportPageClassCreator)
