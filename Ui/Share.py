from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget


def shadow_setup(
    target: QWidget, offset: tuple, blurRadius: int, color: QColor
) -> None:
    # 设置阴影
    effect_shadow = QGraphicsDropShadowEffect(target)  # 创建阴影效果对象
    effect_shadow.setOffset(offset[0], offset[1])  # 阴影的偏移量
    effect_shadow.setBlurRadius(blurRadius)  # 阴影的模糊程度
    effect_shadow.setColor(color)  # 阴影的颜色
    target.setGraphicsEffect(effect_shadow)  # 设置阴影效果
