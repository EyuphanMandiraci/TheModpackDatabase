from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class UsernameSelector(QLineEdit):
    def __init__(self, **kwargs):
        super(UsernameSelector, self).__init__(**kwargs)
        self.setValidator(QRegExpValidator(QRegExp("[A-Za-z0-9_]{0,16}")))
