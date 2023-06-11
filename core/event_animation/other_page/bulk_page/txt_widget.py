from PyQt5.QtCore import QSize, QParallelAnimationGroup, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtWidgets import QWidget


def max_size(widget: QWidget):
    """放大控件"""
    # 放大
    widget_animation_resize = QPropertyAnimation(widget, b"size", widget)  # 创建放大动画对象
    widget_animation_resize.setDuration(600)  # 设置动画持续时间
    widget_animation_resize.setStartValue(QSize(widget.width(), widget.height()))  # 初始位置
    widget_animation_resize.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    widget_animation_resize.setEndValue(
        QSize(
            widget.width(),
            widget.height() + 200
        )
    )  # 结束位置

    # 添加到动画组
    # 串行动画组
    animation_sequent_group = QParallelAnimationGroup(widget)
    animation_sequent_group.addAnimation(widget_animation_resize)

    # 启动动画
    animation_sequent_group.start()


def min_size(widget: QWidget):
    """缩小控件"""
    # 缩小
    widget_animation_resize = QPropertyAnimation(widget, b"size", widget)  # 创建缩小动画对象
    widget_animation_resize.setDuration(800)  # 设置动画持续时间
    widget_animation_resize.setStartValue(QSize(widget.width(), widget.height()))  # 初始位置
    widget_animation_resize.setEasingCurve(QEasingCurve.OutBack)  # 设置动画曲线
    widget_animation_resize.setEndValue(
        QSize(
            widget.width(),
            widget.height() - 200
        )
    )  # 结束位置

    # 添加到动画组
    # 串行动画组
    animation_sequent_group = QParallelAnimationGroup(widget)
    animation_sequent_group.addAnimation(widget_animation_resize)

    # 启动动画
    animation_sequent_group.start()
