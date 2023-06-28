import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QWidget,
)
from creart import create

from Ui.OtherWidget import FixLoginWidget, SteamSettingWidget
from Core.EventJudgment import login_widget_size_button_checked_event
from Core.file_operation import FileOperation
from Core.network_threads import SteamLoginThread


def account_info_widget_right_size_btn(
    widget, add_account_widget, server_status_widget
) -> QCheckBox:
    """
    设置右侧的放大/缩小控件
    :param widget:  承载窗体
    :param add_account_widget:  添加账号的控件
    :param server_status_widget:  服务器状态的控件
    :return:
    """
    size_button = QCheckBox()

    # 单独设置属性
    # 放大_缩小按钮设置, 绑定事件
    size_button.setObjectName("size_button")
    size_button.setFixedSize(32, 32)
    # int类型 当选中时为2,未选中时为0
    size_button.stateChanged.connect(
        lambda state: login_widget_size_button_checked_event(
            state, widget, add_account_widget, server_status_widget
        )
    )

    return size_button


def account_info_widget_right_repair_btn() -> QCheckBox:
    """
    设置右侧修复登录按钮
    :return:
    """
    # 创建按钮
    repair_button = QCheckBox()

    # 下载按钮属性设置
    repair_button.setObjectName("repair_button")
    repair_button.setFixedSize(32, 32)

    # 信号绑定
    repair_button.stateChanged.connect(
        lambda: create(FixLoginWidget).page.setCurrentIndex(3)
    )

    return repair_button


class CardWidget:
    def __init__(self, font: str, refresh: callable, parent: QWidget):
        self.font = font
        self.parent = parent
        self.__file_operation = create(FileOperation)
        self.__refresh_widget = refresh

    @staticmethod
    def __account_info_widget_right_size_btn(
        widget, add_account_widget, server_status_widget
    ) -> QCheckBox:
        """
        设置右侧的放大/缩小控件
        :param widget:  承载窗体
        :param add_account_widget:  添加账号的控件
        :param server_status_widget:  服务器状态的控件
        :return:
        """
        size_button = QCheckBox()

        # 单独设置属性
        # 放大_缩小按钮设置, 绑定事件
        size_button.setObjectName("size_button")
        size_button.setFixedSize(32, 32)
        # int类型 当选中时为2,未选中时为0
        size_button.stateChanged.connect(
            lambda state: login_widget_size_button_checked_event(
                state, widget, add_account_widget, server_status_widget
            )
        )

        return size_button

    def scroll_widget_card_setup(self, account: dict) -> QWidget:
        """
        设置滚动窗体内卡片控件

        :param account:
        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)
        # 设置控件属性
        widget.setObjectName("scroll_widget_card")
        widget.setFixedSize(445, 55)

        # 设置显示名称
        avatar_name = self.__scroll_widget_card_avatar_name(account)
        # 登录时间
        time = self.__scroll_widget_card_time(account)
        # 更多按钮
        other_btn = self.__scroll_widget_card_other_btn(account)

        # 添加到控件
        layout.addWidget(avatar_name, 0, 0, 1, 1)

        layout.addWidget(time, 1, 0, 1, 1, Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(other_btn, 0, 2, 1, 1, Qt.AlignRight)

        layout.setVerticalSpacing(10)

        return widget

    def __scroll_widget_card_avatar_name(self, account_info: dict) -> QWidget:
        """设置账号名称的控件"""
        widget = QWidget()  # 承载窗体
        layout = QGridLayout(widget)  # 创建布局

        # 创建控件
        label = QLabel()
        name_label = QLabel(account_info["cammy_user"])

        # 设置窗体属性
        widget.setFixedSize(300, 20)

        # 设置图标属性
        label.setFixedSize(16, 16)
        label.setObjectName("account_img_label")
        label.setPixmap(
            QPixmap("./img/icon/LoginWidget/account_info/account_name_icon.svg")
        )
        label.setScaledContents(True)

        # 设置名字属性
        name_label.setFixedSize(name_label.width(), 20)
        name_label.setObjectName("account_name_label")
        name_label.setFont(QFont(self.font, 11))

        # 添加到控件
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(name_label, 0, 1, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setHorizontalSpacing(5)

        return widget

    def __scroll_widget_card_time(self, account_info: dict) -> QWidget:
        """
        设置登录时间的控件
        :return:
        """
        widget = QWidget()  # 承载窗体
        layout = QGridLayout(widget)  # 创建布局

        if not account_info["Timestamp"]:
            time = "暂未登录"
        else:
            # 时间戳转换
            time = datetime.datetime.fromtimestamp(
                float(account_info["Timestamp"])
            ).strftime("%Y-%m-%d %H:%M:%S")

        # 创建控件
        img = QLabel()
        label = QLabel(time)

        # 设置窗体属性
        widget.setObjectName("logged_time_widget")
        widget.setFixedSize(155, 14)

        # 设置图标属性
        img.setFixedSize(14, 14)
        img.setObjectName("logged_time")
        img.setPixmap(QPixmap("./img/icon/LoginWidget/account_info/time_icon.svg"))
        img.setScaledContents(True)

        # 设置名字属性
        label.setFixedSize(155, 14)
        label.setObjectName("logged_time")
        label.setFont(QFont(self.font, 8))

        # 添加到控件
        layout.addWidget(img, 0, 0, 1, 1)
        layout.addWidget(label, 0, 1, 1, 1)

        layout.setContentsMargins(0, 0, 0, 5)
        layout.setHorizontalSpacing(5)

        return widget

    def __scroll_widget_card_other_btn(self, account_info: dict) -> QPushButton:
        """
        设置卡片上的其他按钮
        :param account_info:
        :return:
        """
        # 创建控件
        btn = QPushButton()
        btn.setIcon(QIcon("./img/icon/LoginWidget/account_info/other_btn_icon.svg"))
        btn.setFixedSize(24, 24)
        btn.setObjectName("other_btn")

        # 创建菜单
        menu = QMenu(btn)
        # menu.setFixedSize(115, 135)
        menu.setFixedSize(115, 105)

        # 创建菜单项
        menu_login_btn = QAction(
            QIcon("./img/icon/LoginWidget/account_info/action_login_btn.svg"),
            "登录账号",
            menu,
        )
        menu_delete_btn = QAction(
            QIcon("./img/icon/LoginWidget/account_info/action_delete_btn.svg"),
            "删除账号",
            menu,
        )
        menu_skip_email_btn = QAction(
            QIcon("./img/icon/LoginWidget/account_info/unchecked.svg"), "跳过验证", menu
        )

        # 菜单项列表
        menu_list = [menu_login_btn, menu_delete_btn, menu_skip_email_btn]

        # 设置菜单
        menu.setWindowFlags(
            menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        menu.setAttribute(Qt.WA_TranslucentBackground)
        # 设置菜单项可选
        menu_skip_email_btn.setCheckable(True)

        # 循环设置控件
        for i in menu_list:
            i.setFont(QFont(self.font, 12))  # 设置字体
            menu.addAction(i)  # 添加到菜单

        # 读取配置
        self.__read_menu_config(menu_skip_email_btn, account_info)

        # 菜单项槽函数绑定
        menu_login_btn.triggered.connect(
            lambda: self.__other_btn_menu_login_action(menu_login_btn, account_info)
        )
        menu_delete_btn.triggered.connect(
            lambda: self.__other_btn_menu_remove_action(account_info)
        )
        menu_skip_email_btn.triggered.connect(
            lambda: self.__other_btn_menu_skip_action(menu_skip_email_btn, account_info)
        )

        # 设置控件对象名称
        menu.setObjectName("other_btn_menu")

        # 设置按钮菜单
        btn.setMenu(menu)

        return btn

    def __other_btn_menu_login_action(self, action: QAction, account_info: dict):
        """其他按钮的菜单登录账号选项行为槽函数"""
        # 登录线程
        self.login = SteamLoginThread(account_info, self.parent)
        self.login.login_state.connect(
            lambda state, msg: QMessageBox.warning(self.parent, "登录失败", msg)
            if not state
            else None
        )
        self.login.start()
        # 刷新卡密信息
        cammy = self.__file_operation.read_cammy_json()
        for cammy_item in cammy:
            if cammy_item["cammy_user"] == account_info["cammy_user"]:
                cammy_item["Timestamp"] = str(datetime.datetime.now().timestamp())
        self.__file_operation.write_json(self.__file_operation.cammy_data_path, cammy)
        self.__refresh_widget()

    def __other_btn_menu_remove_action(self, account_info: dict):
        """其他按钮的菜单删除账号选项行为槽函数"""
        # 读取卡密
        cammy_list = self.__file_operation.read_cammy_json()
        # 遍历卡密列表删除卡密
        for cammy in cammy_list:
            if cammy["cammy_user"] == account_info["cammy_user"]:
                cammy_list.remove(cammy)
                break
        # 写入卡密文件
        self.__file_operation.write_json(
            self.__file_operation.cammy_data_path, cammy_list
        )
        # 刷新窗体
        self.__refresh_widget()

    def __other_btn_menu_skip_action(self, action: QAction, account_info: dict):
        """其他按钮的菜单跳过验证选项行为槽函数"""
        cammy = self.__file_operation.read_cammy_json()
        if action.isChecked():
            action.setIcon(QIcon("./img/icon/LoginWidget/account_info/check.svg"))
            for cammy_item in cammy:
                if cammy_item["cammy_user"] == account_info["cammy_user"]:
                    cammy_item["skip_email"] = True
                    break
        else:
            action.setIcon(QIcon("./img/icon/LoginWidget/account_info/unchecked.svg"))
            for cammy_item in cammy:
                if cammy_item["cammy_user"] == account_info["cammy_user"]:
                    cammy_item["skip_email"] = False
                    break
        self.__file_operation.write_json(self.__file_operation.cammy_data_path, cammy)
        self.__refresh_widget()

    def __read_menu_config(self, action_list: QAction, account_info: dict):
        """读取卡密设置"""
        cammy_list = self.__file_operation.read_cammy_json()
        for cammy in cammy_list:
            if cammy["cammy_user"] == account_info["cammy_user"]:
                if cammy["skip_email"]:
                    action_list.setChecked(True)
                    action_list.setIcon(
                        QIcon("./img/icon/LoginWidget/account_info/check.svg")
                    )
                else:
                    action_list.setChecked(False)
                    action_list.setIcon(
                        QIcon("./img/icon/LoginWidget/account_info/unchecked.svg")
                    )


def scroll_widget_card_setup(
    account: dict, font: str, refresh: callable, ui: QMainWindow
):
    """卡片"""
    card = CardWidget(font, refresh, ui)
    return card.scroll_widget_card_setup(account)
