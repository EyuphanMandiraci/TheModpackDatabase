import os.path
import traceback

from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent
from PyQt5.QtWidgets import QPushButton, QFileDialog

from utils import log


class SkinSelector(QPushButton):
    def __init__(self, *args, **kwargs):
        super(SkinSelector, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.window = args[0]
        self.setText("Skin Seç veya Sürükle")
        self.resize(len(self.text()) * 8, 30)
        self.move(self.window.width() - self.width(), 60)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        try:
            if e.mimeData().hasUrls():
                if os.path.splitext(e.mimeData().urls()[0].toLocalFile())[1] == ".png" or \
                        os.path.splitext(e.mimeData().urls()[0].toLocalFile())[1] == ".PNG":
                    e.accept()
                else:
                    e.ignore()
            else:
                e.ignore()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def dropEvent(self, e: QDropEvent) -> None:
        try:
            file = e.mimeData().urls()[0].toLocalFile()
            self.setText(os.path.basename(file))
            self.resize(len(self.text()) * 8, 30)
            self.move(self.window.width() - self.width(), 60)
            self.window.skinpath = file
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        try:
            fname, _ = QFileDialog.getOpenFileName(self, "Skin Seç...", "", "PNG Image (*.png)")
            if fname != "":
                self.setText(os.path.basename(fname))
                self.resize(len(self.text()) * 8, 30)
                self.move(self.window.width() - self.width(), 60)
                self.window.skinpath = fname
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))
