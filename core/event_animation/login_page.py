from PyQt5.QtCore import QEasingCurve, QPoint, QSize
from PyQt5.QtWidgets import QWidget

from core.event_animation.AnimationObject import Animation


def login_account_animation_max(
    info_widget: QWidget, account_widget: QWidget, status_widget: QWidget
):
    """
    将账号信息控件最大化，其他控件隐藏
    :param info_widget: 账号信息控件
    :param account_widget: 输入账密控件
    :param status_widget: 状态信息控件
    """
    # 创建移动动画
    animation_obj = Animation(info_widget)
    move_animation = animation_obj.setPos(
        time=700,
        easing_curve=QEasingCurve.OutBack,
        start_value=QPoint(info_widget.x(), info_widget.y()),
        end_value=QPoint(info_widget.x(), info_widget.y() - 205),
    )
    # 创建放大动画
    resize_animation = animation_obj.setSize(
        time=500,
        easing_curve=QEasingCurve.OutBack,
        start_value=QSize(info_widget.width(), info_widget.height()),
        end_value=QSize(info_widget.width(), info_widget.height() + 200),
    )
    # 添加到串行动画组
    animation_group = animation_obj.addAnimationGroup(
        [move_animation, resize_animation], parallel_mod=True
    )
    # 输入账密控件,和状态信息控件隐藏
    animation_group.finished.connect(
        lambda: (account_widget.setHidden(True), status_widget.setHidden(True))
    )
    # 启动动画
    animation_group.start()


def login_account_animation_min(
    info_widget: QWidget, account_widget: QWidget, status_widget: QWidget
):
    """
    将账号信息控件最小化，其他控件显示
    :param info_widget: 账号信息控件
    :param account_widget: 输入账密控件
    :param status_widget: 状态信息控件
    """
    # 创建移动动画
    animation_obj = Animation(info_widget)
    move_animation = animation_obj.setPos(
        time=700,
        easing_curve=QEasingCurve.OutBack,
        start_value=QPoint(info_widget.x(), info_widget.y()),
        end_value=QPoint(info_widget.x(), info_widget.y() + 205),
    )
    # 创建放大动画
    resize_animation = animation_obj.setSize(
        time=500,
        easing_curve=QEasingCurve.OutBack,
        start_value=QSize(info_widget.width(), info_widget.height()),
        end_value=QSize(info_widget.width(), info_widget.height() - 200),
    )
    # 添加到串行动画组
    animation_group = animation_obj.addAnimationGroup(
        [move_animation, resize_animation], parallel_mod=True
    )
    # 输入账密控件,和状态信息控件隐藏
    animation_group.stateChanged.connect(
        lambda: (account_widget.setHidden(False), status_widget.setHidden(False))
    )
    # 启动动画
    animation_group.start()
