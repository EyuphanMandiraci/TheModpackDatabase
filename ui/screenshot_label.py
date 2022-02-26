from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui, QtCore


class ScreenshotLabel(QLabel):
    clicked = QtCore.pyqtSignal(str)
    double_clicked = QtCore.pyqtSignal(str)

    def __init__(self, *args, path):
        super(ScreenshotLabel, self).__init__(*args)
        self.path = path

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit(self.path)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.double_clicked.emit(self.path)

