from PyQt5.QtWidgets import QLineEdit


def init(cls):
    cls.username_selector = QLineEdit(cls)
    cls.username_selector.move(800, 0)
    cls.username_selector.setPlaceholderText("Username")
    cls.username_selector.setStyleSheet("background:rgba(185,187,190,255)")


def get_username(cls):
    return cls.username_selector.getText()