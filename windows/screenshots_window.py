import os
import subprocess
import sys

from PyQt5.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QIcon, QResizeEvent, QKeyEvent
from PyQt5.QtCore import Qt
import requests

from ui.screenshot_label import ScreenshotLabel


class ScreenshotsWindow(QMainWindow):
    def __init__(self, image_path):
        super(ScreenshotsWindow, self).__init__()
        self.resize(1000, 600)
        self.setWindowTitle("Screenshots")
        self.mainwidget = QWidget()
        self.glayout = QGridLayout()
        self.scrollarea = QScrollArea()
        self.setCentralWidget(self.scrollarea)
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get("https://mpdb.xyz/static/logo.webp").content)
            self.setWindowIcon(QIcon(pixmap))
        except:
            print("Logo Yüklenemedi")

        self.sses = []
        self.pms = []

        counter = 0
        for index, item in enumerate(sorted(os.listdir(f"{image_path}"))):
            ss = ScreenshotLabel(path=f"{image_path}/{item}")
            pm = QPixmap(f"{image_path}/{item}")
            pm = pm.scaledToWidth(self.width() // 2, Qt.SmoothTransformation)
            ss.setPixmap(pm)
            ss.resize(pm.width(), pm.height())
            ss.double_clicked.connect(self.openScreenshot)
            self.pms.append(pm)
            self.sses.append(ss)
            if index % 2 == 0:
                ss.setAlignment(Qt.AlignLeft)
            else:
                ss.setAlignment(Qt.AlignRight)
            if index % 2 == 0:
                self.glayout.addWidget(ss, int(counter), 0)
            else:
                self.glayout.addWidget(ss, int(counter), 1)
            counter += 0.5
        self.mainwidget.setLayout(self.glayout)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.mainwidget)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        for index, ss in enumerate(self.sses):
            p = self.pms[index].scaledToWidth(self.width() // 2, Qt.SmoothTransformation)
            ss.setPixmap(p)
            ss.resize(p.width(), p.height())

    def openScreenshot(self, path):
        subprocess.call(["start" if sys.platform == "win32" else "xdg-open", path])
