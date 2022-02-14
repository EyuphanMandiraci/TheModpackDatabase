from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QMouseEvent, QTextCursor, QKeyEvent


class LogTextEdit(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super(LogTextEdit, self).__init__(*args, **kwargs)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        return

    def keyPressEvent(self, e: QKeyEvent) -> None:
        return

    def addTextLn(self, text):
        self.insertPlainText(str(text) + "\n")

    def addText(self, text):
        self.insertPlainText(str(text))
