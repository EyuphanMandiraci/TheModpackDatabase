from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


def init(cls, text=""):
    cls.run_minecraft_info = QLabel(text, cls)
    cls.run_minecraft_info.setAlignment(Qt.AlignRight)
    cls.run_minecraft_info.move(900, 30)


def set_text(cls, text):
    cls.run_minecraft_info.setText(text)
    cls.run_minecraft_info.resize(len(text) * 8, cls.run_minecraft_info.height())