from PyQt5.QtWidgets import QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QMouseEvent, QIcon
from PyQt5 import QtCore
import requests


class ScreenshotsButton(QPushButton):
    clicked = QtCore.pyqtSignal(QPushButton)

    def __init__(self, parent):
        super(ScreenshotsButton, self).__init__(parent=parent)
        image_data = requests.get("https://mpdb.xyz/static/image-files.png").content
        image = QPixmap()
        image.loadFromData(image_data)
        icon = QIcon()
        icon.addPixmap(image)
        self.setIcon(icon)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.clicked.emit(self)
