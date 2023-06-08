from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QGridLayout
from creart import create

from core.file_operation import FileOperation
from ui.share import shadow_setup


def path_page(font: str) -> QWidget:
    """
    路径信息控件
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
    title = QLabel("路径设置")
    title.setFont(QFont(font, 10))
    title.setObjectName("set_title_label")

    # 添加到布局
    title_layout.addWidget(title)
    title_layout.setContentsMargins(30, 0, 0, 0)
    title_layout.setVerticalSpacing(1)

    """卡片控件"""
    # 创建卡片控件，并设置属性
    path_info_wgt = QWidget()
    path_layout = QGridLayout(path_info_wgt)

    # 设置最大高度
    path_info_wgt.setFixedHeight(60)

    # 设置对象名称，用于QSS定位
    path_info_wgt.setObjectName("author_info_widget")

    # 创建子控件
    new_steam_path = dw_info_widget_steam_path(font)

    # 添加到控件
    path_layout.addWidget(new_steam_path, 0, 0, 1, 1)
    path_layout.setContentsMargins(15, 20, 5, 10)

    # 添加阴影
    shadow_setup(
        path_info_wgt, (2, 2), 10, QColor(29, 190, 245, 60)
    )

    """添加到控件"""
    layout.addWidget(title_wgt, 0, 0, 1, 1)
    layout.addWidget(path_info_wgt, 1, 0, 1, 1)
    layout.setVerticalSpacing(1)

    return widget


def dw_info_widget_steam_path(font: str):
    """
    旧版steam路径
    :return:
    """
    """构建控件"""

    # 创建控件
    widget = QWidget()
    layout = QGridLayout(widget)

    # 设置控件属性
    # widget.setFixedSize(260, 25)

    # 创建子控件
    label = QLabel("新版Steam路径：")
    edit = QLineEdit("未检测到路径")
    button = QPushButton(
        QIcon("./img/other_widget/dw/choose_file.svg"),
        "手动选择"
    )

    # 创建子控件列表
    widget_list = [label, edit, button]

    # 设置控件属性
    label.setObjectName("steam_path_label")
    edit.setObjectName("steam_path_edit")
    button.setObjectName("steam_path_button")

    # 设置共有属性
    for i in widget_list:
        i.setFont(QFont(font, 10))

    # 设置label独有属性
    label.setFixedSize(100, 20)

    # 设置edit独有属性
    edit.setFixedSize(280, 20)
    edit.setReadOnly(True)  # 设置只读

    # 设置button独有属性
    button.setFixedSize(75, 20)
    button.setIconSize(QSize(14, 14))

    # 添加到控件
    layout.addWidget(label, 0, 0, 1, 1)
    layout.addWidget(edit, 0, 1, 1, 1)
    layout.addWidget(button, 0, 2, 1, 1)
    layout.setContentsMargins(20, 5, 20, 5)

    """功能实现"""
    # 读取配置文件中的新版Steam路径
    if not create(FileOperation).config_data["steam_set"]["path"] is None:
        edit.setText(create(FileOperation).steam_path.__str__().capitalize())

    return widget
