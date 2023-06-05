from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QWidget
from PyQt5.QtGui import QColor


def shadow_setup(target: QWidget):
    # 设置阴影
    effect_shadow = QGraphicsDropShadowEffect(target)  # 创建阴影效果对象
    effect_shadow.setOffset(2, 2)  # 阴影的偏移量
    effect_shadow.setBlurRadius(10)  # 阴影的模糊程度
    effect_shadow.setColor(QColor(29, 190, 245, 60))  # 阴影的颜色
    target.setGraphicsEffect(effect_shadow)  # 设置阴影效果
