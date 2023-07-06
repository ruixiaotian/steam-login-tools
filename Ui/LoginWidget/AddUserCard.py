from abc import ABC

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QAction,
    QCompleter,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)
from creart import add_creator, exists_module, create
from creart.creator import AbstractCreator, CreateTargetInfo

from Config import BaseConfig
from Core.file_operation import FileOperation
from Ui.OtherWidget.BulkImportWidget import BulkImportWidget
from Ui.Share import shadow_setup


class AddUserCard:
    user_edit: QLineEdit
    password_edit: QLineEdit
    ssfn_edit: QLineEdit

    def initialize(self, parent, font: str, refresh: callable) -> None:
        """初始化"""
        self.parent = parent
        self.font = font
        self.refresh = refresh

    def add_user_setup(self):
        """
        设置添加账号的控件

        :return:
        """
        widget = QWidget()
        layout = QGridLayout(widget)

        # 创建控件
        self.user_edit, self.password_edit, self.ssfn_edit = [
            QLineEdit() for _ in range(3)
        ]
        save_button, bulk_import_btn = QPushButton("保存"), QPushButton("批量导入")
        edit_list = [self.user_edit, self.password_edit, self.ssfn_edit]

        # 创建列表
        edit_obj_name_list = ["user_edit", "password_edit", "ssfn_edit"]
        place_text_list = ["USER-账号", "PASSWORD-密码", "SSFN(如果有)"]
        icon_path_list = [
            "./img/icon/LoginWidget/add_account/user.svg",
            "./img/icon/LoginWidget/add_account/pwd.svg",
            "./img/icon/LoginWidget/add_account/ssfn.svg",
        ]

        # 单独设置属性
        widget.setObjectName("add_account_widget")  # 设置控件的名字

        # 按钮设置
        save_button.setObjectName("save_button")
        save_button.setFixedSize(80, 30)
        save_button.setFont(QFont(self.font, 11))

        bulk_import_btn.setObjectName("bulk_import_btn")
        bulk_import_btn.setFixedSize(80, 30)
        bulk_import_btn.setFont(QFont(self.font, 11))

        # 编辑框设置
        self.password_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码输入模式
        # 设置联想器
        self.__ssfn_edit_completer()
        # 设置密码框行为
        self.__pwd_edit_visible_state()

        # 循环设置对象名称
        for edit, name in zip(edit_list, edit_obj_name_list):
            edit.setObjectName(name)  # 设置对象名称

        # 循环设置属性
        for edit, text in zip(edit_list, place_text_list):
            # 设置输入框通用属性
            edit.setFixedSize(200, 30)
            edit.setPlaceholderText(text)
            edit.setFont(QFont(self.font, 8))
        for edit, path in zip(edit_list, icon_path_list):
            # 循环设置输入款图标
            edit.addAction(QIcon(path), QLineEdit.LeadingPosition)

        """绑定按钮信号"""
        # 保存按钮
        save_button.clicked.connect(lambda: self.__save_btn_trough())
        # 批量导入按钮
        bulk_import_btn.clicked.connect(
            lambda: create(BulkImportWidget).page.setCurrentIndex(4)
        )

        # 添加到布局
        for num, edit, policy in zip(
            range(edit_list.__len__()), edit_list, [Qt.AlignHCenter for _ in range(3)]
        ):
            layout.addWidget(edit, num, 0, 1, 2, policy)

        layout.setContentsMargins(0, 35, 0, 20)
        layout.addWidget(save_button, 3, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(bulk_import_btn, 3, 1, 1, 1, Qt.AlignLeft)
        layout.setHorizontalSpacing(20)

        # 设置阴影
        shadow_setup(widget, (2, 3), 25, QColor(29, 190, 245, 80))

        return widget

    def __save_btn_trough(self) -> None:
        """保存按钮的槽函数"""
        if self.user_edit.text() and self.password_edit.text() != str():
            self.__account_save_file()
            self.refresh()
            _ = [
                edit.clear()
                for edit in [self.user_edit, self.password_edit, self.ssfn_edit]
            ]

    def __pwd_edit_visible_state(self) -> None:
        """密码编辑框模式切换槽函数"""

        def judgement():
            # 定义判断函数
            if self.password_edit.echoMode() == QLineEdit.PasswordEchoOnEdit:
                # 如果是密码输入模式,则切换回普通模式
                self.password_edit.setEchoMode(QLineEdit.Normal)  # 设置普通模式
                action.setIcon(
                    QIcon("./img/icon/LoginWidget/add_account/invisible.svg")
                )
            else:
                # 如果是普通输入模式,则切换回密码输入模式
                self.password_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 设置密码模式
                action.setIcon(QIcon("./img/icon/LoginWidget/add_account/visible.svg"))

        # 设置行为
        action = QAction(self.password_edit)
        action.setIcon(QIcon("./img/icon/LoginWidget/add_account/visible.svg"))
        action.triggered.connect(judgement)

        # 添加到行为
        self.password_edit.addAction(action, QLineEdit.TrailingPosition)

    def __ssfn_edit_completer(self) -> None:
        """ssfn自动补全槽函数"""
        # 创建一个字符串列表作为 自动补全 的候选项
        ssfn_list = create(FileOperation).read_json_file("./data/ssfn_list.json")
        # 创建一个 QCompleter 对象，并将字符串列表设置为其自动补全的候选项
        completer = QCompleter(ssfn_list, self.ssfn_edit)
        completer.setObjectName("ssfn_edit_completer")
        completer.setCompletionMode(QCompleter.InlineCompletion)  # 设置自动补全模式
        # 将 QCompleter 对象设置为 QLineEdit 的自动补全器
        self.ssfn_edit.setCompleter(completer)

    def __account_save_file(self) -> None:
        """
        保存按钮槽函数
        :return:
        """
        config = create(BaseConfig).AccountDataDictTemplate
        config["cammy_user"] = self.user_edit.text()
        config["cammy_pwd"] = self.password_edit.text()
        config["cammy_ssfn"] = self.ssfn_edit.text()

        create(FileOperation).modify_json(
            create(FileOperation).cammy_data_path, config, add=True
        )


class AddUserCardCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("Ui.LoginWidget.AddUserCard", "AddUserCard"),)

    # 静态方法available()，用于检查模块"AddUserCard"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Ui.LoginWidget.AddUserCard")

    # 静态方法create()，用于创建AddUserCard类的实例，返回值为AddUserCard对象。
    @staticmethod
    def create(create_type: [AddUserCard]) -> AddUserCard:
        return AddUserCard()


add_creator(AddUserCardCreator)
