from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout

from ui.other_widget.FixLoginWidget.fix_page.fix_63 import fix_63_layout
from ui.share import shadow_setup


def fix_page(font: str, ui: QMainWindow) -> QWidget:
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
    title = QLabel("修复错误")
    title.setFont(QFont(font, 10))
    title.setObjectName("other_page_min_title_label")

    # 添加到布局
    title_layout.addWidget(title, 0, 0, 1, 1, Qt.AlignLeft)
    title_layout.setContentsMargins(30, 0, 0, 0)
    title_layout.setVerticalSpacing(1)

    """卡片控件"""
    # 创建卡片控件，并设置属性
    fix_wgt = QWidget()
    fix_layout = QGridLayout(fix_wgt)

    # 设置最大高度
    fix_wgt.setFixedHeight(65)

    # 设置对象名称，用于QSS定位
    fix_wgt.setObjectName("author_info_widget")

    # 子控件
    fix_63 = fix_63_layout(font, ui)

    # 添加到控件
    fix_layout.addLayout(fix_63, 0, 0, 1, 1)
    fix_layout.setContentsMargins(30, 20, 30, 5)

    # 添加阴影
    shadow_setup(
        fix_wgt, (2, 2), 10, QColor(29, 190, 245, 60)
    )

    """添加到控件"""
    layout.addWidget(title_wgt, 0, 0, 1, 1)
    layout.addWidget(fix_wgt, 1, 0, 1, 1)
    layout.setVerticalSpacing(0)

    return widget
