from PyQt5.QtWidgets import QComboBox


def none_test():
    pass


def init(cls, values, text_change_connect=none_test):
    cls.modpack_selector = QComboBox(cls)
    cls.modpack_selector.addItems(values)
    cls.modpack_selector.move(0, 70)
    cls.modpack_selector.currentTextChanged.connect(text_change_connect)
    cls.modpack_selector.setStyleSheet("background:rgba(185,187,190,255)")
    cls.modpack_selector.adjustSize()


def addItems(cls, value_list):
    cls.modpack_selector.addItems(value_list)


def currentText(cls):
    return cls.modpack_selector.currentText()

