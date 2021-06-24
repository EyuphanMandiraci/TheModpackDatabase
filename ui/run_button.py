from PyQt5.QtWidgets import QPushButton


def none_test():
    pass


def init(cls, text, clicked_connect=none_test):
    cls.run_button = QPushButton(text, cls)
    cls.run_button.move(900, 0)
    cls.run_button.clicked.connect(clicked_connect)
    cls.run_button.setStyleSheet("background:rgba(185,187,190,255)")
    cls.run_button.setEnabled(False)