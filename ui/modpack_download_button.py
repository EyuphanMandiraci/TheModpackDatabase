from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore, QtGui


class ModpackDlButton(QPushButton):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, text, mp_name, *args):
        super(ModpackDlButton, self).__init__(text, *args)
        self.setObjectName(mp_name)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.clicked.emit(self.objectName())
