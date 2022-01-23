from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore


class StatusText(QLabel):
    text_changed = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(StatusText, self).__init__(*args, **kwargs)
        self.text_changed.connect(self.textChange)

    def setText(self, a0: str) -> None:
        super().setText(a0)
        self.text_changed.emit(a0)

    def textChange(self):
        self.resize(len(self.text()) * 8, self.height())
