from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont


def fix_63_widget(font: str):
    """修复登录错误63"""
    # 创建布局
    layout = QGridLayout()

    # 创建控件

    # 左方label
    label = QLabel("一键修复登录错误 代码:63")
    label.setFont(QFont(font, 8))

