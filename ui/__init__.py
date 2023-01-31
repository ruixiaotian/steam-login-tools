#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/25 0:41
# @Author  : 桥话语权
# @File    : __init__.py.py
# @Software: PyCharm
"""
* 程序UI
"""

import sys
from PyQt5.Qt import *
from core import FileOperation


class SteamLoginUI(QMainWindow):
    """程序UI的绘制"""

    def __init__(self) -> None:
        """初始化程序设定"""
        super(SteamLoginUI, self).__init__()
        self.setup_window()
        self.setup_font()
        self.setup_form()
        self.setup_layout()
        self.read_qss_file()

    def setup_window(self) -> None:
        """设定窗体各类参数

        :return: None
        """
        self.setFixedSize(700, 450)  # 设定窗体大小
        self.setWindowTitle("Steam上号器")  # 设定窗口名
        self.setWindowIcon(QIcon("./img/icon/icon.ico"))  # 设定窗体图标
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗体属性为透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # 隐藏框架,并且设置为主窗体

    def read_qss_file(self) -> None:
        """读取QSS文件

        :return: None
        """
        with open('./QSS/ui.qss', 'r', encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    def setup_font(self) -> None:
        """窗体字体获取

        :return: None
        """
        self.font_english_name = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(r"./font/Crossover-2.ttf"))[0]
        self.font_chinese_name = QFontDatabase.applicationFontFamilies(
            QFontDatabase.addApplicationFont(r"./font/锐字荣光粗黑简1.0.ttf"))[0]

    def setup_form(self) -> None:
        """窗体设定

        :return: None
        """
        # 透明窗体
        self.base_widget = QWidget()  # 创建透明窗口
        self.base_widget.setObjectName("base_widget")  # 设置对象名称
        self.base_layout = QGridLayout()  # 创建透明窗口布局
        self.base_widget.setLayout(self.base_layout)  # 设置布局
        self.base_widget.setAttribute(Qt.WA_TranslucentBackground)  # 隐藏背景

        # 主窗体
        self.main_widget = QWidget()  # 创建主窗体
        self.main_widget.setObjectName("main_widget")  # 设置主窗体对象名称
        self.base_layout.addWidget(self.main_widget)  # 添加到布局

        self.setCentralWidget(self.base_widget)  # 设置窗口主部件

        # 添加阴影
        effect_shadow = QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(0, 0)  # 偏移
        effect_shadow.setBlurRadius(10)  # 阴影半径
        effect_shadow.setColor(Qt.gray)  # 阴影颜色
        self.main_widget.setGraphicsEffect(effect_shadow)  # 将设置套用到widget窗口中

    def setup_layout(self) -> None:
        """设定窗体内布局

        :return: None
        """
        layout = QGridLayout()  # 创建网格布局
        layout.addLayout(self.setup_left_list(), 0, 0, 2, 1)
        layout.addLayout(self.setup_top_button(), 0, 1, 1, 1)
        layout.addLayout(self.setup_right_windows(), 1, 1, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(layout)  # 设置窗体内布局

    def setup_left_list(self) -> QLayout:
        """设置左边列表

        :return: QLayout
        """
        layout = QGridLayout()  # 创建布局
        self.left_widget = QWidget()  # 创建控件
        # 设置控件
        self.left_widget.setFixedSize(180, 432)  # 设置固定大小
        self.left_widget.setObjectName("left_widget")  # 设置对象名称

        # 设置动图
        left_head_img = QLabel()  # 创建标签
        left_head_img.setAlignment(Qt.AlignCenter)  # 设置标签居中
        left_head_img_movie = QMovie(r"./img/gif/Steam上号器UI.gif")  # 设置动图
        left_head_img_movie.setScaledSize(QSize(180, 90))  # 设置动图大小
        left_head_img.setMovie(left_head_img_movie)  # 添加到标签
        left_head_img.movie().start()  # 开始动画

        # 设置列表
        list_widget_layout = QVBoxLayout()
        list_widget = QListWidget()
        list_widget.setObjectName("list_widget")  # 设置对象名称
        list_widget.setFixedSize(150, 220)  # 设置固定大小
        list_widget.setFont(QFont(self.font_chinese_name, 16))  # 设置字体和大小
        # 创建项
        item_steam_login = QListWidgetItem("账号登录")  # 创建控件
        item_network_acceleration = QListWidgetItem("网络加速")
        item_tools = QListWidgetItem("功能设置")
        for i in [item_steam_login, item_network_acceleration, item_tools]:
            # 循环设置属性
            i.setTextAlignment(Qt.AlignCenter)
            list_widget.addItem(i)
        list_widget_layout.addWidget(list_widget)  # 添加到布局
        list_widget_layout.setContentsMargins(15, 0, 0, 10)  # 设置内间距

        # 设置控件布局
        widget_layout = QVBoxLayout(self.left_widget)
        widget_layout.addWidget(left_head_img)
        widget_layout.addLayout(list_widget_layout)
        widget_layout.setContentsMargins(0, 0, 0, 70)
        widget_layout.setSpacing(2)

        # 添加到布局
        layout.addWidget(self.left_widget, 0, 0, 1, 1)
        return layout

    def setup_top_button(self) -> QLayout:
        """设置窗口顶部关闭和最小化按钮

        :return: QLayout
        """
        layout = QGridLayout()  # 创建布局
        # 创建控件
        exit_button = QPushButton()
        min_show_button = QPushButton()
        # 控件设置
        exit_button.setObjectName("exit_button")  # 对象名称
        min_show_button.setObjectName("min_show_button")
        exit_button.setFixedSize(18, 18)  # 设置大小
        min_show_button.setFixedSize(18, 18)
        # 设置按钮功能
        exit_button.clicked.connect(self.close)
        min_show_button.clicked.connect(self.showMinimized)
        # 添加到布局
        layout.setContentsMargins(420, 15, 10, 0)
        layout.addWidget(min_show_button, 0, 1, 1, 1)
        layout.addWidget(exit_button, 0, 2, 1, 1)
        return layout

    def setup_right_windows(self) -> QLayout:
        """右边切换窗体设置

        :return: QLayout
        """
        # 创建布局及控件
        layout = QGridLayout()
        self.stacked_widget = QStackedWidget()
        # 设置控件
        self.stacked_widget.setObjectName("right_stacked_widget")
        self.stacked_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.stacked_widget.setMaximumSize(500, 400)
        # 添加页面
        self.stacked_widget.addWidget(self.setup_steam_login_widget())
        # self.stacked_widget.addWidget(self.net_hasten_widget())
        # self.stacked_widget.addWidget(self.setting_widget())

        layout.addWidget(self.stacked_widget, 0, 0, 1, 1)
        layout.setContentsMargins(0, 15, 0, 0)

        return layout

    def setup_steam_login_widget(self) -> QWidget:
        """账号登录界面

        :return: QWidget
        """
        widget = QWidget()  # 创建窗体控件
        layout = QGridLayout(widget)
        # 设置子窗体
        login_Widget = QWidget()
        login_layout = QGridLayout(login_Widget)  # 设置登录窗体
        self.login_list_layout = QVBoxLayout()  # 设置布局

        # 判断是否为初始化
        if not FileOperation().json_is_empty():
            self.login_list_layout.addWidget(self.null_cammy_widget_found(), Qt.AlignTop)

        login_layout.addLayout(self.login_list_layout, 0, 0, 1, 1)

        # 设置切换窗体
        self.page_widget = self.setup_login_widget_page()
        self.page_widget.addWidget(login_Widget)
        self.page_widget.addWidget(self.setup_login_widget_cammy())
        self.page_widget.addWidget(self.setup_login_widget_user_and_pwd())

        # 添加到布局
        layout.addWidget(self.setup_login_widget_button(), 0, 0, 1, 1)
        layout.addWidget(self.page_widget, 1, 0, 1, 1)

        return widget

    def null_cammy_widget_found(self) -> QScrollArea:
        """如果没有卡密信息则调用此函数

        :return: QScrollArea
        """
        null_widget = QWidget()  # 创建控件
        null_widget.setFixedSize(425, 120)  # 设置控件大小
        null_widget.setObjectName("null_widget")
        null_widget_layout = QGridLayout(null_widget)  # 创建布局

        null_label = QLabel("暂无账号噢")  # 创建卡片
        null_label.setObjectName("null_label")
        null_label.setAlignment(Qt.AlignCenter)  # 设置文字居中对齐
        null_label.setFont(QFont(self.font_chinese_name, 24))  # 设置字体及字体大小

        null_widget_layout.addWidget(null_label, 0, 0, 1, 1, Qt.AlignCenter)  # 添加到布局
        scroll = QScrollArea()  # 创建滚动控件
        scroll.setObjectName("scroll")  # 设置对象名称
        scroll.setAlignment(Qt.AlignHCenter)
        scroll.setWidget(null_widget)  # 设置滚动页面

        return scroll

    def setup_login_widget_page(self) -> QStackedWidget:
        """登录界面的切换窗体

        :return: QStackedWidget
        """
        page_widget = QStackedWidget()  # 创建切换窗体
        page_widget.setFixedSize(450, 290)
        page_widget.setObjectName("steam_login_page_widget")

        return page_widget

    def setup_login_widget_button(self) -> QWidget:
        """创建登录界面按钮以及设置按钮属性样式

        :return: QWidget
        """
        btn_widget = QWidget()  # 按钮窗体
        btn_widget.setFixedSize(450, 65)
        # 设置按钮窗体
        btn_widget.setObjectName("steam_login_btn_widget")
        btn_layout = QHBoxLayout(btn_widget)
        cammy_btn = QPushButton("卡密模式")
        user_and_pwd = QPushButton("账密模式")
        del_data_btn = QPushButton("清除数据")
        open_file_btn = QPushButton("打开数据")

        for i, name in zip([cammy_btn, user_and_pwd, del_data_btn, open_file_btn],
                           ["cammy_btn", "user_and_pwd", "del_data_btn", "open_file_btn"]):
            # 设置其控件
            if i == cammy_btn:
                cammy_btn.clicked.connect(lambda: self.page_widget.setCurrentIndex(1))
            if i == user_and_pwd:
                user_and_pwd.clicked.connect(lambda: self.page_widget.setCurrentIndex(2))
            i.setFont(QFont(self.font_chinese_name, 13))
            i.setObjectName(name)
            i.setFixedSize(95, 45)
            btn_layout.addWidget(i)

        # del_data_btn.clicked.connect(self.delete_data)  # TODO: 此方法未定义
        # open_file_btn.clicked.connect(self.open_file)  # TODO: 此方法未定义

        return btn_widget

    def setup_login_widget_cammy(self) -> QWidget:
        """创建登录界面卡密模式窗体

        :return: QWidget
        """
        cammy_widget = QWidget()  # 创建窗体
        # 设置卡密模式窗体
        cammy_layout = QGridLayout(cammy_widget)
        # 创建控件
        cammy_label = QLabel("LOGIN STEAM")
        cammy_edit = QLineEdit()
        cammy_ok_btn = QPushButton("添加")
        cammy_exit_btn = QPushButton("返回")
        # 设置控件
        for i, name in zip([cammy_label, cammy_edit, cammy_ok_btn, cammy_exit_btn],
                           ["cammy_label", "cammy_edit", "cammy_ok_btn", "cammy_exit_btn"]):
            i.setObjectName(name)
            if i == cammy_label:
                i.setFont(QFont(self.font_english_name, 24))
                i.setFixedSize(300, 80)
                i.setAlignment(Qt.AlignCenter)
            if i == cammy_edit:
                i.setFont(QFont(self.font_english_name, 13))
                i.setPlaceholderText("USER----PASSWORD----SSFN")
                i.setFixedSize(400, 30)
                i.textEdited.connect(lambda text:
                                     cammy_edit.setFont(QFont(self.font_english_name, 7))
                                     if text else
                                     cammy_edit.setFont(QFont(self.font_english_name, 13))
                                     )
                i.setClearButtonEnabled(True)
                i.setAlignment(Qt.AlignCenter)
            if i in [cammy_ok_btn, cammy_exit_btn]:
                i.setFixedSize(80, 40)
                i.setFont(QFont(self.font_chinese_name, 13))
                if i == cammy_ok_btn:
                    # TODO:需要一个添加Json的功能
                    i.clicked.connect(lambda: self.cammy_add_json("cammy", cammy_edit.text()))
                if i == cammy_exit_btn:
                    cammy_exit_btn.clicked.connect(lambda: self.page_widget.setCurrentIndex(0))
        # 添加到布局
        cammy_layout.addWidget(cammy_label, 0, 0, 1, 4, Qt.AlignCenter)
        cammy_layout.addWidget(cammy_edit, 1, 0, 1, 4, Qt.AlignCenter)
        cammy_layout.addItem(QSpacerItem(10, 10), 2, 0, 1, 2)
        cammy_layout.addWidget(cammy_ok_btn, 2, 2, 1, 1, Qt.AlignCenter)
        cammy_layout.addWidget(cammy_exit_btn, 2, 1, 1, 1, Qt.AlignCenter)
        cammy_layout.addItem(QSpacerItem(10, 10), 2, 3, 1, 1)

        return cammy_widget

    def setup_login_widget_user_and_pwd(self) -> QWidget:
        """创建登录界面账密模式窗体

        :return:
        """
        user_and_pwd_widget = QWidget()
        # 设置账密模式窗体
        user_and_pwd_widget_layout = QGridLayout(user_and_pwd_widget)
        form_layout = QGridLayout()
        # 创建控件
        user_and_pwd_label = QLabel("LOGIN STEAM")
        user_line_edit, pwd_line_edit, ssfn_line_edit = QLineEdit(), QLineEdit(), QLineEdit()
        user_and_pwd_ok_btn, user_and_pwd_exit_btn = QPushButton("添加"), QPushButton("返回")
        widget_list = [user_line_edit, pwd_line_edit, ssfn_line_edit,
                       user_and_pwd_ok_btn, user_and_pwd_exit_btn, user_and_pwd_label]
        obj_name_list = ["user_line_edit", "pwd_line_edit", "ssfn_line_edit",
                         "user_and_pwd_ok_btn", "user_and_pwd_exit_btn", "user_and_pwd_label"]
        for i, name, row, column in zip(widget_list, obj_name_list, [0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0]):
            i.setObjectName(name)
            if i == user_and_pwd_label:
                i.setFont(QFont(self.font_english_name, 24))
                i.setFixedSize(300, 80)
                i.setAlignment(Qt.AlignCenter)
            if i in [user_line_edit, pwd_line_edit, ssfn_line_edit]:
                i.setFont(QFont(self.font_english_name, 10))
                i.setFixedSize(280, 30)
                i.setAlignment(Qt.AlignLeft)
                i.setPlaceholderText(["USER", "PASSWORD", "SSFN"][row])
                form_layout.addWidget(i, row, column, 1, 1, Qt.AlignCenter)
                form_layout.setRowMinimumHeight(row, 30)
            if i in [user_and_pwd_ok_btn, user_and_pwd_exit_btn]:
                if i == user_and_pwd_ok_btn:
                    i.clicked.connect(lambda: (
                        self.cammy_add_json("up", user_line_edit.text(), pwd_line_edit.text(), ssfn_line_edit.text()),
                        user_line_edit.clear(), pwd_line_edit.clear(), ssfn_line_edit.clear()))
                if i == user_and_pwd_exit_btn:
                    i.clicked.connect(lambda: self.page_widget.setCurrentIndex(0))
                i.setFixedSize(80, 40)
                i.setFont(QFont(self.font_chinese_name, 13))

        user_and_pwd_widget_layout.addWidget(user_and_pwd_label, 0, 0, 1, 4, Qt.AlignCenter)
        user_and_pwd_widget_layout.addLayout(form_layout, 1, 0, 1, 4, Qt.AlignCenter)
        user_and_pwd_widget_layout.addItem(QSpacerItem(10, 3), 2, 0, 1, 1)
        user_and_pwd_widget_layout.addWidget(user_and_pwd_exit_btn, 2, 1, 1, 1, Qt.AlignCenter)
        user_and_pwd_widget_layout.addWidget(user_and_pwd_ok_btn, 2, 2, 1, 1, Qt.AlignCenter)
        user_and_pwd_widget_layout.addItem(QSpacerItem(10, 3), 2, 3, 1, 1)

        return user_and_pwd_widget

    def cammy_add_json(self, mod: str, *args: list | str) -> bool:
        """处理用户输入的卡密,并且判断是否要写入文件
        :param mod ['cammy' | ''up']
        :param *args 传入的参数
        :return: bool
        """
        if mod == "cammy":
            args = args[0].split('----')
            if len(args) == 3:
                json_data = {
                    args[0]: {
                        'cammy_user': args[0],
                        'cammy_pwd': args[1],
                        'cammy_ssfn': args[2],
                        'steam64_id': '',
                        'AccountName': '',
                        'PersonaName': '',
                        'WantsOfflineMode': '',
                        'SkipOfflineModeWarning': '',
                        'MostRecent': '',
                        'Timestamp': '',
                    }
                }
                FileOperation().write_json_file(json_data)
            else:
                return False
        elif mod == "up":
            if len(args) == 3:
                user, pwd, ssfn = args
                json_data = {
                    user: {
                        'cammy_user': user,
                        'cammy_pwd': pwd,
                        'cammy_ssfn': ssfn,
                        'steam64_id': '',
                        'AccountName': '',
                        'PersonaName': '',
                        'WantsOfflineMode': '',
                        'SkipOfflineModeWarning': '',
                        'MostRecent': '',
                        'Timestamp': '',
                    }
                }
                FileOperation().write_json_file(json_data)
            else:
                return False
        else:
            return False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """重构鼠标按下事件函数,进行鼠标跟踪以及获取相对位置

        :param event:
        :return: None
        """
        if event.button() == Qt.LeftButton:
            # 如果按下按钮为左键
            self._mouse_flag = True  # 设置鼠标跟踪开关为True
            self.m_pos = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """重构鼠标移动事件函数,进行监控鼠标移动并且判断是否拖动窗口

        :param event:
        :return: None
        """
        if Qt.LeftButton and self._mouse_flag:
            # 如果是左键按下且鼠标跟踪打卡
            self.move(event.globalPos() - self.m_pos)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """重构鼠标松开事件函数,进行监控鼠标状态

        :param event:
        :return: None
        """
        self._mouse_flag = False  # 设置鼠标跟踪为关


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SteamLoginUI()
    win.show()
    sys.exit(app.exec())
