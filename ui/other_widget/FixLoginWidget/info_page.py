from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QGridLayout

from ui.share import shadow_setup


def info_page(font: str) -> QWidget:
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
    title = QLabel("什么是修复登录?")
    title.setFont(QFont(font, 10))
    title.setObjectName("set_title_label")

    # 添加到布局
    title_layout.addWidget(title)
    title_layout.setContentsMargins(30, 0, 0, 0)
    title_layout.setVerticalSpacing(1)

    """卡片控件"""
    # 创建卡片控件，并设置属性
    fix_info_wgt = QWidget()
    fix_info_layout = QGridLayout(fix_info_wgt)

    # 设置最大高度
    fix_info_wgt.setFixedHeight(185)

    # 设置对象名称，用于QSS定位
    fix_info_wgt.setObjectName("author_info_widget")

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
    fix_info_layout.addWidget(info_edit, 0, 0, 1, 1)
    fix_info_layout.setContentsMargins(30, 20, 30, 5)

    # 添加阴影
    shadow_setup(
        fix_info_wgt, (2, 2), 10, QColor(29, 190, 245, 60)
    )

    """添加到控件"""
    layout.addWidget(title_wgt, 0, 0, 1, 1)
    layout.addWidget(fix_info_wgt, 1, 0, 1, 1)
    layout.setVerticalSpacing(0)

    return widget
