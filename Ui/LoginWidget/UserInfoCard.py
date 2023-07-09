import datetime
from abc import ABC

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
from creart import add_creator, create, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo

from Core.EventJudgment import userInfoSizeBtnTrough
from Core.file_operation import FileOperation
from Core.NetworkThreads import SteamLoginThread
from Ui.OtherWidget import FixLoginWidget


class UserInfoCard:
    def initialize(
        self, widget: QWidget, add_user_card: QWidget, server_state_card: QWidget
    ) -> None:
        self.base_widget = widget
        self.add_user_card = add_user_card
        self.server_state_card = server_state_card

    def size_btn(self) -> QCheckBox:
        """设置右侧的放大/缩小控件"""
        size_button = QCheckBox()

        # 单独设置属性
        # 放大_缩小按钮设置, 绑定事件
        size_button.setObjectName("size_button")
        size_button.setFixedSize(32, 32)
        # int类型 当选中时为2,未选中时为0
        size_button.stateChanged.connect(
            lambda state: userInfoSizeBtnTrough(state, self.base_widget, self.add_user_card, self.server_state_card)
        )

        return size_button

    @staticmethod
    def repair_btn() -> QCheckBox:
        """设置右侧修复登录按钮"""
        # 创建按钮
        repair_button = QCheckBox()

        # 修复按钮属性设置
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
        self.__refresh_widget = refresh

    def scroll_widget_card_setup(self, account: dict) -> QWidget:
        """设置滚动窗体内卡片控件"""
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
        """设置登录时间的控件 """
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
        """设置卡片上的其他按钮"""
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

    def __other_btn_menu_login_action(self, action: QAction, account_info: dict) -> None:
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
        cammy = create(FileOperation).read_cammy_json()
        for cammy_item in cammy:
            if cammy_item["cammy_user"] == account_info["cammy_user"]:
                cammy_item["Timestamp"] = str(datetime.datetime.now().timestamp())
        create(FileOperation).write_json(create(FileOperation).cammy_data_path, cammy)
        self.__refresh_widget()

    def __other_btn_menu_remove_action(self, account_info: dict) -> None:
        """其他按钮的菜单删除账号选项行为槽函数"""
        # 读取卡密
        cammy_list = create(FileOperation).read_cammy_json()
        # 遍历卡密列表删除卡密
        for cammy in cammy_list:
            if cammy["cammy_user"] == account_info["cammy_user"]:
                cammy_list.remove(cammy)
                break
        # 写入卡密文件
        create(FileOperation).write_json(
            create(FileOperation).cammy_data_path, cammy_list
        )
        # 刷新窗体
        self.__refresh_widget()

    def __other_btn_menu_skip_action(self, action: QAction, account_info: dict) -> None:
        """其他按钮的菜单跳过验证选项行为槽函数"""
        cammy = create(FileOperation).read_cammy_json()
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
        create(FileOperation).write_json(create(FileOperation).cammy_data_path, cammy)
        self.__refresh_widget()

    @staticmethod
    def __read_menu_config(action_list: QAction, account_info: dict) -> None:
        """读取卡密设置"""
        cammy_list = create(FileOperation).read_cammy_json()
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
) -> QWidget:
    """卡片"""
    card = CardWidget(font, refresh, ui)
    return card.scroll_widget_card_setup(account)


class UserInfoCardCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LoginWidget.UserInfoCard", "UserInfoCard"),)

    # 静态方法available()，用于检查模块"UserInfoCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginWidget.UserInfoCard")

    # 静态方法create()，用于创建UserInfoCard类的实例，返回值为UserInfoCard对象。
    @staticmethod
    def create(create_type: [UserInfoCard]) -> UserInfoCard:
        return UserInfoCard()


add_creator(UserInfoCardCreator)
