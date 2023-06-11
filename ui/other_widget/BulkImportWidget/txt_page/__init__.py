from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, QLineEdit, QSizePolicy

from ui.share import shadow_setup
from ui.other_widget.BulkImportWidget.txt_page.file_choose import file_choose


def txt_page(font: str) -> QWidget:
    """
    修复错误介绍控件
    :return:
    """
    # 创建大控件
    widget = QWidget()
    layout = QGridLayout(widget)

    """标题控件"""
    # 创建控件
    title_wgt = QWidget()
    title_layout = QGridLayout(title_wgt)

    # 创建子控件
    title = QLabel("从TXT导入")
    title.setFont(QFont(font, 10))
    title.setFixedHeight(10)
    title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    title.setObjectName("other_page_min_title_label")

    # 添加到布局
    title_layout.addWidget(title)
    title_layout.setContentsMargins(30, 0, 0, 0)
    title_layout.setVerticalSpacing(0)

    """卡片控件"""
    # 创建卡片控件，并设置属性
    txt_wgt = QWidget()
    txt_layout = QGridLayout(txt_wgt)

    # 设置最大高度
    # txt_wgt.resize(180, 60)
    txt_wgt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # 设置对象名称，用于QSS定位
    txt_wgt.setObjectName("author_info_widget")

    # 创建子控件
    file_choose_wgt = file_choose(font, widget)

    # 添加到控件
    txt_layout.addLayout(file_choose_wgt, 0, 0, 1, 1, Qt.AlignTop)

    # 添加阴影
    shadow_setup(
        txt_wgt, (2, 2), 10, QColor(29, 190, 245, 60)
    )

    """添加到控件"""
    layout.addWidget(title_wgt, 0, 0, 1, 1)
    layout.addWidget(txt_wgt, 1, 0, 1, 1)
    layout.setVerticalSpacing(0)

    return widget


