from abc import ABC

from PyQt5.QtCore import QSize, QEasingCurve
from creart import exists_module, add_creator, create
from creart.creator import AbstractCreator, CreateTargetInfo

from Core.EventAnimation.AnimationObject import Animation


class TextImportPageAnimation:
    """从TXT导入页面动画设置"""

    def __init__(self) -> None:
        self.page_state = True

        # 获取控件
        from Ui.OtherWidget.BulkImportWidget.TextImportPage import TextImportPage
        from Ui.OtherWidget.BulkImportWidget.TextImportPage.TableCard import (
            TextImportTabelCard,
        )

        self.card_wgt = create(TextImportPage).widget
        self.data_func_control_list = create(TextImportPage).date_func_control_list
        self.table_wgt = create(TextImportTabelCard).widget

    def card_max_size(self) -> None:
        """放大控件"""
        # 判断状态
        if self.page_state:
            animation_obj = Animation(self.card_wgt)
            resize_animation = animation_obj.setSize(
                time=200,
                easing_curve=QEasingCurve.InOutExpo,
                start_value=QSize(self.card_wgt.width(), self.card_wgt.height()),
                end_value=QSize(self.card_wgt.width() + 5, self.card_wgt.height() + 26),
            )
            # 添加到串行动画组并启动
            animation_group = animation_obj.addAnimationGroup(
                resize_animation, parallel_mod=True
            )
            # 链接槽函数拉起下一步
            animation_group.finished.connect(
                lambda: [
                    control.setHidden(False) for control in self.data_func_control_list
                ]
            )
            animation_group.start()
            # 设置状态
            self.page_state = False

    def card_min_size(self) -> None:
        """缩小控件"""
        # 判断状态
        if not self.page_state:
            # 执行动画
            [control.setHidden(True) for control in self.data_func_control_list]
            animation_obj = Animation(self.card_wgt)
            resize_animation = animation_obj.setSize(
                time=200,
                easing_curve=QEasingCurve.OutCirc,
                start_value=QSize(self.card_wgt.width(), self.card_wgt.height()),
                end_value=QSize(self.card_wgt.width() - 5, self.card_wgt.height() - 26),
            )
            # 添加到串行动画组并启动
            animation_group = animation_obj.addAnimationGroup(
                resize_animation, parallel_mod=True
            )
            animation_group.start()
            # 设置状态
            self.page_state = True

    def table_enter_move(self) -> None:
        """QTableWidget入场动画"""
        if not self.page_state:
            self.table_wgt.setHidden(False)  # 显示表格

    def table_exit_move(self) -> None:
        """QTableWidget出场"""
        self.table_wgt.setHidden(True)  # 显示表格


class TextImportPageAnimationClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (
        CreateTargetInfo(
            "Core.EventAnimation.other_page.bulk_page.txt_widget",
            "TextImportPageAnimation",
        ),
    )

    # 静态方法available()，用于检查模块"BulkImportWidget"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("Core.EventAnimation.other_page.bulk_page.txt_widget")

    # 静态方法create()，用于创建TextImportPageAnimation类的实例，返回值为TextImportPageAnimation对象。
    @staticmethod
    def create(create_type: [TextImportPageAnimation]) -> TextImportPageAnimation:
        return TextImportPageAnimation()


add_creator(TextImportPageAnimationClassCreator)
