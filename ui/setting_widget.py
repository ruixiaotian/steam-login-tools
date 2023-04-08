"""
设置页面页面
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout, QGraphicsDropShadowEffect, QSpacerItem, \
    QSizePolicy, QVBoxLayout, QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt
from pathlib import Path

from core.event_judgment import setting_widget_size_button_checked_event


class SettingWidget:

    def __init__(self, parent: QMainWindow, font: str):
        self.parent = parent
        self.font = font

    def setting_widget_setup(self):
        """
        设置界面
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        # 设置属性
        widget.resize(400, 500)
        widget.setObjectName('setting_widget')

        # 获取控件
        software_info_widget = self.software_info()
        software_setting_widget = self.software_setting()

        # 添加控件
        layout.addWidget(software_info_widget, 0, 0, 1, 1)
        layout.addWidget(software_setting_widget, 1, 0, 1, 1)
        # layout.addItem(QSpacerItem(10, 100, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 0, 1, 1)

        return widget

    def software_info(self):
        """
        软件信息控件
        :return:
        """
        # 创建基础控件，并设置属性
        self.soft_info_widget = QWidget(self.parent)
        layout = QGridLayout(self.soft_info_widget)

        # 设置最大高度
        self.soft_info_widget.setFixedHeight(120)

        # 设置对象名称，用于QSS定位
        self.soft_info_widget.setObjectName("author_info_widget")

        """创建子控件"""
        img = self.__software_info_widget_img()
        title = self.__software_info_widget_title()
        msg = self.__software_info_widget_msg()

        """添加到控件"""
        layout.setContentsMargins(30, 20, 30, 15)
        layout.addWidget(img, 0, 0, 4, 1, Qt.AlignLeft)
        layout.addItem(QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Minimum), 0, 0, 1, 1)
        layout.addWidget(title, 1, 1, 1, 1, Qt.AlignRight)
        layout.addWidget(msg, 2, 1, 1, 1, Qt.AlignRight)
        layout.addItem(QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Minimum), 3, 0, 1, 1)

        # 添加阴影
        self.shadow_setup(self.soft_info_widget)

        return self.soft_info_widget

    @staticmethod
    def __software_info_widget_img():
        """设置软件头像"""
        __img_path = Path("./img/setting_widget/github.svg")
        __pixmap = QPixmap(64, 64)
        __pixmap.load(str(__img_path))

        img = QLabel()
        img.setObjectName("software_info_img")
        img.setPixmap(__pixmap)
        img.setFixedSize(64, 64)
        img.setScaledContents(True)

        return img

    def __software_info_widget_title(self):
        """软件名字"""
        title = QLabel("Steam Login Tool")
        title.setObjectName("software_info_title")
        title.setFont(QFont(self.font, 18))

        return title

    def __software_info_widget_msg(self):
        """软件信息"""
        a = "<a style='text-decoration: none; color: #1DBEF5' href='https://github.com/ruixiaotian/steam-login-tools'>GitHub</a>"
        msg = QLabel(
            f"这是一个来自于 {a} 的开源项目 "
        )
        msg.setOpenExternalLinks(True)
        msg.setObjectName("software_info_msg")
        msg.setFont(QFont(self.font, 10))

        return msg

    def software_setting(self):
        """
                软件设置控件
                :return:
                """
        # 创建基础控件，并设置属性
        self.soft_setting_widget = QWidget(self.parent)
        layout = QGridLayout(self.soft_setting_widget)

        # 设置最大高度
        self.soft_setting_widget.setMinimumHeight(330)

        # 设置对象名称，用于QSS定位
        self.soft_setting_widget.setObjectName("software_setting_widget")

        """创建子控件"""
        right_widget = self.__right_widget()

        """添加到控件"""
        layout.addLayout(right_widget, 0, 0, 1, 1, Qt.AlignRight)

        # 添加阴影
        self.shadow_setup(self.soft_setting_widget)

        return self.soft_setting_widget

    def __right_widget(self):
        """右侧按钮控件"""
        layout = QVBoxLayout()

        # 添加到控件
        layout.addWidget(self.__right_size_widget())

        return layout

    def __right_size_widget(self):
        """右侧按钮设置"""
        size_button = QCheckBox()

        # 单独设置属性
        # 放大_缩小按钮设置, 绑定事件
        size_button.setObjectName('size_button')
        size_button.setFixedSize(32, 32)
        size_button.setChecked(False)
        # int类型 当选中时为0,未选中时为2
        size_button.stateChanged.connect(
            lambda state: setting_widget_size_button_checked_event(state, self.soft_info_widget,
                                                                   self.soft_setting_widget))

        return size_button

    def __server_setting(self):
        """服务器设置"""
        # 创建布局
        layout = QVBoxLayout()

        # 创建控件
        title = QLabel("授权服务器设置")
        list_widget = QListWidget()

        # 设置控件属性
        title.setObjectName("server_setting_title")
        list_widget.setObjectName("server_setting_list_widget")

        """创建选项"""

        # 授权服务器1
        item1 = QListWidgetItem("授权服务器 1 号")
        item1_widget = QWidget()

    @staticmethod
    def shadow_setup(target: QWidget):
        # 设置阴影
        effect_shadow = QGraphicsDropShadowEffect(target)  # 创建阴影效果对象
        effect_shadow.setOffset(2, 3)  # 阴影的偏移量
        effect_shadow.setBlurRadius(25)  # 阴影的模糊程度
        effect_shadow.setColor(QColor(29, 190, 245, 80))  # 阴影的颜色
        target.setGraphicsEffect(effect_shadow)  # 设置阴影效果
