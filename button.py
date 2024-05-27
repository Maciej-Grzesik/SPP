from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Button(QPushButton):
    def __init__(self, name: str, parent=None):
        super(Button, self).__init__(parent)
        self.setStyleSheet(
            "QPushButton {"
            "   border: 1px solid; "
            "   border-radius: 2px;"
            "   border-color: #ffffff;"
            "   color: #ffffff;"
            "}"
            "QPushButton:hover {"
            "   background-color: rgba(255, 255, 255, 0.1);"
            "}"
            "QPushButton:pressed {"
            "   background-color: rgba(255, 255, 255, 0.2);"
            "}"
        )
        self.setText(name)
        self.setFixedSize(150, 50)

        self.animation = QPropertyAnimation(self, b'size')
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    # def enterEvent(self, event):
    #     super(Button, self).enterEvent(event)
    #
    #     target_size = QSize(self.width() + 25, self.height() + 10)
    #     self.animation.setEndValue(target_size)
    #     self.animation.start()
    #     print(self.width(), self.height())
    #
    # def leaveEvent(self, event):
    #     super(Button, self).leaveEvent(event)
    #
    #     target_size = QSize(self.width() - 25, self.height() - 10)
    #     self.animation.setEndValue(target_size)
    #     self.animation.start()
    #     print(self.width(), self.height())
