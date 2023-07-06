import shutil
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QMainWindow, QMessageBox, QPushButton
from creart import create

from Core.file_operation import FileOperation
from Ui.Share import shadow_setup


def fix_63_layout(font: str, ui: QMainWindow) -> QGridLayout:
    """修复登录错误63"""
    # 创建布局
    layout = QGridLayout()

    """创建控件"""

    # 左方label
    label = QLabel("一键修复登录错误 代码:63")
    label.setFont(QFont(font, 10))
    label.setObjectName("fix_63_label")

    # 右方按钮
    btn = QPushButton("一键修复")
    btn.setFont(QFont(font, 10))
    btn.setObjectName("fix_63_btn")
    btn.setFixedSize(70, 25)
    btn.clicked.connect(lambda: fix_63_btn_trough(ui))
    shadow_setup(btn, (1, 1), 5, QColor(29, 190, 245, 40))

    """添加到布局"""
    layout.addWidget(label, 0, 0, 1, 1, Qt.AlignLeft)
    layout.addWidget(btn, 0, 1, 1, 1, Qt.AlignRight)

    return layout


def fix_63_btn_trough(ui: QMainWindow) -> None:
    """一键修复的槽函数"""
    try:
        # 删除steam根目录下的config文件夹
        config_path = Path(create(FileOperation).steam_path) / "config"
        if config_path.exists() and config_path.is_dir():
            shutil.rmtree(config_path.__str__())
        QMessageBox.information(ui, "修复成功", "操作完成,请登录验证是否成功!")
    except Exception as e:
        QMessageBox.information(ui, "修复失败", e.__str__())
