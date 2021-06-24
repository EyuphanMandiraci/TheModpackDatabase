from PyQt5.QtWidgets import QComboBox


def none_test():
    pass


def init(cls, values, text_change_connect=none_test):
    cls.ram_selector = QComboBox(cls)
    cls.ram_selector.addItems(values)
    cls.ram_selector.move(0, 100)
    cls.ram_selector.currentTextChanged.connect(text_change_connect)
    cls.ram_selector.setStyleSheet("background:rgba(185,187,190,255)")


def get_ram(cls):
    return int(cls.ram_selector.currentText().replace(" GB", ""))
