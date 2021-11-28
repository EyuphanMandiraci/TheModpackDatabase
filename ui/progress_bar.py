from PyQt5.QtWidgets import QProgressBar


def init(cls):
    cls.progress_bar = QProgressBar(cls)
    cls.progress_bar.setStyleSheet("background:rgba(185,187,190,255)")
    cls.progress_bar.move(0, cls.height() - 15)
    cls.progress_bar.resize(cls.width(), 15)
