from PyQt5.QtCore import QEasingCurve, QPoint, QSize
from PyQt5.QtWidgets import QWidget

from Core.EventAnimation.AnimationObject import Animation


def setting_account_animation_max(info_widget: QWidget, setting_widget: QWidget):
    """
    将账号信息控件最大化，其他控件隐藏
    :param info_widget: 账号信息控件
    :param setting_widget: 设置控件
    :return:
    """
    # 创建移动动画
    animation_obj = Animation(setting_widget)
    move_animation = animation_obj.setPos(
        time=1200,
        easing_curve=QEasingCurve.OutBack,
        start_value=QPoint(setting_widget.x(), setting_widget.y()),
        end_value=QPoint(setting_widget.x(), setting_widget.y() - 125),
    )
    # 创建放大动画
    resize_animation = animation_obj.setSize(
        time=1000,
        easing_curve=QEasingCurve.OutBack,
        start_value=QSize(setting_widget.width(), setting_widget.height()),
        end_value=QSize(setting_widget.width(), setting_widget.height() + 125),
    )
    # 添加到串行动画组
    animation_group = animation_obj.addAnimationGroup(
        [move_animation, resize_animation], parallel_mod=True
    )
    # 输入账密控件,和状态信息控件隐藏
    animation_group.finished.connect(lambda: info_widget.setHidden(True))
    # 启动动画
    animation_group.start()


def setting_account_animation_min(
    info_widget: QWidget,
    setting_widget: QWidget,
):
    """
    将账号信息控件最小化，其他控件隐藏
    :param info_widget: 账号信息控件
    :param setting_widget: 设置控件
    :return:
    """
    # 创建移动动画
    animation_obj = Animation(setting_widget)
    move_animation = animation_obj.setPos(
        time=1200,
        easing_curve=QEasingCurve.OutBack,
        start_value=QPoint(setting_widget.x(), setting_widget.y()),
        end_value=QPoint(setting_widget.x(), setting_widget.y() + 125),
    )
    # 创建放大动画
    resize_animation = animation_obj.setSize(
        time=1000,
        easing_curve=QEasingCurve.OutBack,
        start_value=QSize(setting_widget.width(), setting_widget.height()),
        end_value=QSize(setting_widget.width(), setting_widget.height() - 125),
    )
    # 添加到串行动画组
    animation_group = animation_obj.addAnimationGroup(
        [move_animation, resize_animation], parallel_mod=True
    )
    # 输入账密控件,和状态信息控件隐藏
    animation_group.stateChanged.connect(lambda: info_widget.setHidden(False))
    # 启动动画
    animation_group.start()
