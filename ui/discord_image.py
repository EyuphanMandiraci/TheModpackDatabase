from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from requests import get


def init(cls, image, fromweb=True):
    if fromweb:
        cls.discord_image = QImage()
        cls.discord_image.loadFromData(get(image).content)
        cls.discord_image_label = QLabel(cls)
        cls.discord_image_pixmap = QPixmap(cls.discord_image)
    else:
        cls.discord_image_label = QLabel(cls)
        cls.discord_image_pixmap = QPixmap(image)
    cls.discord_image_pixmap = cls.discord_image_pixmap.scaled(64, 64)
    cls.discord_image_label.setPixmap(cls.discord_image_pixmap)
    cls.discord_image_label.resize(64, 64)
    cls.discord_image_label.setMouseTracking(True)
