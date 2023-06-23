from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QSizePolicy, QPushButton

from Ui.OtherWidget.BulkImportWidget.TextImportPage.Variant import FilePathFunc
from Ui.Share import shadow_setup


class TextImportPage:

    def __init__(self, font):
        self.font = font
        self.widget = QWidget()

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
        txt_wgt = QWidget()
        txt_layout = QGridLayout(txt_wgt)
        # 设置最大高度
        txt_wgt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置对象名称，用于QSS定位
        txt_wgt.setObjectName("author_info_widget")
        # 创建子控件
        file_choose_wgt = self.file_choose()
        # 添加到控件
        txt_layout.addLayout(file_choose_wgt, 0, 0, 1, 1, Qt.AlignTop)
        # 添加阴影
        shadow_setup(txt_wgt, (2, 2), 10, QColor(29, 190, 245, 60))

        return txt_wgt

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
        self.file_path_setup()

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

    def file_path_setup(self):
        """文件路径输入框设置属性"""

        # 设置文本内边距
        self.file_path_edit.setTextMargins(2, 1, 1, 2)
        # 设置文本占位文字
        self.file_path_edit.setPlaceholderText("请选择文件路径")
        # 设置只读
        self.file_path_edit.setReadOnly(True)

        # 链接按钮槽函数
        self.file_choose_btn.clicked.connect(
            lambda: FilePathFunc().chose_file_path_trough(self.widget, self.file_path_edit)
        )