from PyQt5.QtCore import QSize, QPoint, QEasingCurve
from PyQt5.QtWidgets import QWidget

from core.event_animation.AnimationObject import Animation


page_state = True


def max_size(widget: QWidget):
    """放大控件"""
    # 声明全局变量
    global page_state
    # 判断状态
    if page_state:
        animation_obj = Animation(widget)
        resize_animation = animation_obj.setSize(
            time=600, easing_curve=QEasingCurve.OutBack,
            start_value=QSize(widget.width(), widget.height()),
            end_value=QSize(widget.width(), widget.height() + 320)
        )
        # 添加到串行动画组并启动
        animation_group = animation_obj.addAnimationGroup(resize_animation, parallel_mod=True)
        animation_group.start()
        # 设置状态
        page_state = False


def min_size(widget: QWidget):
    """缩小控件"""
    # 声明全局变量
    global page_state
    # 判断状态
    if not page_state:
        animation_obj = Animation(widget)
        resize_animation = animation_obj.setSize(
            time=800, easing_curve=QEasingCurve.InBack,
            start_value=QSize(widget.width(), widget.height()),
            end_value=QSize(widget.width(), widget.height() - 320)
        )
        # 添加到串行动画组并启动
        animation_group = animation_obj.addAnimationGroup(resize_animation, parallel_mod=True)
        animation_group.start()
        # 设置状态
        page_state = True
