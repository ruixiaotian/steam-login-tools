from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QTextEdit, QWidget

from Ui.Share import shadow_setup


def info_page(font: str) -> QWidget:
    """修复错误介绍控件"""
    # 创建大控件
    widget = QWidget()
    layout = QGridLayout(widget)

    """标题控件"""
    # 创建控件
    title_wgt = QWidget()
    title_layout = QGridLayout(title_wgt)

    # 创建子控件
    title = QLabel("什么是批量导入?")
    title.setFont(QFont(font, 10))
    title.setObjectName("other_page_min_title_label")

    # 添加到布局
    title_layout.addWidget(title)
    title_layout.setContentsMargins(30, 0, 0, 0)
    title_layout.setVerticalSpacing(1)

    """卡片控件"""
    # 创建卡片控件，并设置属性
    bulk_info_wgt = QWidget()
    bulk_info_layout = QGridLayout(bulk_info_wgt)

    # 设置最大高度
    bulk_info_wgt.setFixedHeight(185)

    # 设置对象名称，用于QSS定位
    bulk_info_wgt.setObjectName("author_info_widget")

    # 创建子控件
    info_edit = QTextEdit()

    # 设置属性
    info_edit.setObjectName("fix_info_edit")
    info_edit.setReadOnly(True)
    info_edit.setFont(QFont(font, 9))

    # 添加文本
    with open("./data/fix_info_edit_content.html", "r", encoding="utf-8") as f:
        info_edit.setHtml(f.read())

    # 添加到控件
    bulk_info_layout.addWidget(info_edit, 0, 0, 1, 1)
    bulk_info_layout.setContentsMargins(30, 20, 30, 5)

    # 添加阴影
    shadow_setup(bulk_info_wgt, (2, 2), 10, QColor(29, 190, 245, 60))

    """添加到控件"""
    layout.addWidget(title_wgt, 0, 0, 1, 1)
    layout.addWidget(bulk_info_wgt, 1, 0, 1, 1)
    layout.setVerticalSpacing(0)

    return widget
