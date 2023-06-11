from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, \
    QLineEdit, QPushButton
from PyQt5.QtCore import Qt

from creart import create

from ui.share import shadow_setup
from ui.other_widget.BulkImportWidget.txt_page.file_choose.Variant import FilePathCompletion


def file_choose(font: str, txt_page: QWidget) -> QGridLayout:
    """
    txt导入,文件选择项
    :param font: 字体
    :param txt_page: 控件
    :return: QGridLayout
    """

    # 创建布局
    layout = QGridLayout()

    # 创建控件
    file_label = QLabel("文件路径:")
    file_path = QLineEdit()
    file_choose_btn = QPushButton("选择文件")

    # 添加到列表
    obj_list = [file_label, file_path, file_choose_btn]
    obj_name = ["file_label", "file_path", "file_choose_btn"]

    # 设置属性
    _ = [obj.setFont(QFont(font)) for obj in obj_list]
    _ = [obj.setObjectName(name) for obj, name in zip(obj_list, obj_name)]

    # 设置输入框属性
    file_path_setup(file_path, txt_page)

    # 设置按钮属性
    file_choose_btn.setFixedSize(65, 20)
    shadow_setup(file_choose_btn, (1, 1), 5, QColor(29, 190, 245, 40))

    # 添加到布局
    layout.addWidget(file_label, 0, 0, 1, 1, Qt.AlignVCenter)
    layout.addWidget(file_path, 0, 1, 1, 1, Qt.AlignVCenter)
    layout.addWidget(file_choose_btn, 0, 2, 1, 1, Qt.AlignVCenter)

    layout.setContentsMargins(20, 10, 20, 0)
    layout.setHorizontalSpacing(8)

    return layout


def file_path_setup(file_path: QLineEdit, txt_page: QWidget):
    """文件路径输入框设置属性"""
    # 设置文本内边距
    file_path.setTextMargins(2, 0, 3, 0)
    # 设置文本占位文字
    file_path.setPlaceholderText("请输入或选择文件路径")
    # 设置清空按钮
    file_path.setClearButtonEnabled(True)
    # 设置联想器
    completion = FilePathCompletion(file_path)
    file_path.textEdited.connect(lambda text: completion.path_completion(text))
    file_path.editingFinished.connect(lambda: completion.file_judgement(txt_page))

