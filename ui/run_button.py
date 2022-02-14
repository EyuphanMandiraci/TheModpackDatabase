from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QMouseEvent


class RunButton(QPushButton):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(RunButton, self).__init__(*args, **kwargs)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.clicked.emit(self.objectName())
