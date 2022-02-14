# Libraries
import traceback
from typing import Union

import requests
from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton, QPlainTextEdit
from PyQt5 import QtCore
import sys
from pathlib import Path
from requests import get

# UI Components
from ui.modpack_download_button import ModpackDlButton
from ui.modpack_text import ModpackText
from ui.progress_bar import ProgressBar
from ui.status_text import StatusText
from ui.modpack_selector import ModpackSelector
from ui.run_button import RunButton
from ui.log_text_edit import LogTextEdit
from ui.username_selector import UsernameSelector
from ui.ram_selector import RamSelector
from ui.skin_selector import SkinSelector

# Utils
from utils import data
from utils import log

# Threads
from threads import download_thread
from threads import run_thread


class MPDB(QMainWindow):
    skin_selector: SkinSelector
    ram_selector: RamSelector
    user_selector: UsernameSelector
    log_text: LogTextEdit
    dialog: Union[QDialog, QDialog]
    run_button: RunButton
    mp_selector: ModpackSelector
    status: StatusText
    mp_dl_button: ModpackDlButton
    mp_text: ModpackText
    progress_bar: ProgressBar

    def __init__(self):
        super(MPDB, self).__init__()
        self.mp_buttons = []
        self.setFixedSize(QSize(1000, 600))
        self.setWindowTitle("TheModpackDatabase")
        data.create_data()
        self.data = data.get_data()
        self.run_thread = None
        self.skinpath = None
        Path("mpdblogs").mkdir(exist_ok=True)

    def initUI(self):
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get("https://mpdb.xyz/static/logo.webp").content)
            self.setWindowIcon(QIcon(pixmap))
        except:
            print("Logo Yüklenemedi")
        self.mp_selector = ModpackSelector(self)
        self.mp_selector.resize(QSize(200, 50))
        self.mp_selector.move(QPoint(0, 0))
        self.modpacksloop()
        for mp in self.data["downloaded"]:
            self.mp_selector.addItem(mp)
            for btn in self.mp_buttons:
                if btn.objectName() == mp:
                    btn.setEnabled(False)
        self.mp_selector.addItem("Test")
        self.status = StatusText("", self)
        self.status.move(QPoint(0, 500))
        self.progress_bar = ProgressBar(self)
        self.progress_bar.move(QPoint(0, self.height() - self.progress_bar.height()))
        self.progress_bar.resize(QSize(self.width(), self.progress_bar.height()))
        self.progress_bar.hide()
        self.run_button = RunButton("Run", self)
        self.run_button.resize(QSize((len(self.run_button.text()) * 8) + 5, self.run_button.height()))
        self.run_button.move(QPoint(self.width() - self.run_button.width(), 0))
        self.run_button.clicked.connect(self.runGame)
        self.mpselectorChanged(self.mp_selector.currentText())
        self.mp_selector.currentTextChanged.connect(self.mpselectorChanged)
        self.user_selector = UsernameSelector(parent=self)
        self.user_selector.resize(QSize(160, 30))
        self.user_selector.move(QPoint(self.width() - self.user_selector.width(), 30))
        self.ram_selector = RamSelector(self)
        self.ram_selector.resize(QSize(200, 50))
        self.ram_selector.move(QPoint(200, 0))
        self.skin_selector = SkinSelector(self)

    def mpselectorChanged(self, mp_name):
        self.run_button.setObjectName(mp_name)
        self.run_button.setText(f"Run {mp_name}")
        self.run_button.resize(QSize((len(self.run_button.text()) * 8) + 5, self.run_button.height()))
        self.run_button.move(QPoint(self.width() - self.run_button.width(), 0))

    def modpacksloop(self):
        try:
            modpacks = get("https://mpdb.xyz/api/modpack").json()
        except Exception as e:
            modpacks = []
            log.error(traceback.format_tb(e.__traceback__))
        count = 50
        for i in modpacks:
            self.mp_text = ModpackText(i["mp_name"], self)
            self.mp_text.move(0, count)
            self.mp_text.setToolTip(i["mp_author"])
            self.mp_dl_button = ModpackDlButton("Download", self.mp_text.text(), self)
            self.mp_dl_button.move(100, count)
            self.mp_dl_button.clicked.connect(self.downloadModpack)
            self.mp_buttons.append(self.mp_dl_button)
            count += self.mp_text.height()

    def downloadModpack(self, mp_name):
        def downloadCompleted(thread):
            self.progress_bar.hide()
            thread.wait()
            data.write_to_data(mp_name)
            self.data = data.get_data()
            for mp in self.data["downloaded"]:
                for btn in self.mp_buttons:
                    if btn.objectName() == mp:
                        btn.setEnabled(False)
            self.mp_selector.addItem(mp_name)

        try:
            mp_info = get(f"https://mpdb.xyz/api/modpack?mp_name={mp_name}").json()[0]
            file_name = mp_info["mp_file"]
            server_info = get(f"https://mpdb.xyz/api/server?name={mp_info['mp_server']}").json()[0]
            dlth = download_thread.DownloadThread(server_info["url"] + file_name, mp_info, parent=self)
            dlth.download_signal.connect(self.changeValue)
            dlth.download_completed.connect(downloadCompleted)
            dlth.start()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def changeValue(self, percent, downloaded, total):
        self.progress_bar.setValue(percent)
        self.progress_bar.show()

    def runGame(self, mp_name):
        def log_(text):
            try:
                self.log_text.addTextLn(text)
            except Exception as e:
                print(e)

        def stop():
            self.run_thread.stop()
            try:
                self.dialog.close()
            except Exception as e:
                print("")
            self.run_button.setEnabled(True)

        try:
            mp_info = get(f"https://mpdb.xyz/api/modpack?mp_name={mp_name}").json()[0]
            self.run_button.setEnabled(False)
            self.run_thread = run_thread.RunThread(mp_info, parent=self)
            self.run_thread.stopped.connect(stop)
            self.run_thread.logging.connect(log_)
            self.run_thread.run_started.connect(self.openLogDialog)
            self.run_thread.start()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.run_thread is not None:
            self.run_thread.killMinecraft()

    def openLogDialog(self):
        try:
            self.dialog = QDialog()
            self.dialog.setWindowFlags(
                                  QtCore.Qt.WindowMinimizeButtonHint |
                                  QtCore.Qt.WindowCloseButtonHint)
            self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.dialog.resize(QSize(800, 600))
            self.log_text = LogTextEdit(self.dialog)
            self.log_text.resize(QSize(800, 600))
            self.log_text.setReadOnly(True)
            self.log_text.setLineWrapMode(QPlainTextEdit.LineWrapMode())
            self.dialog.setWindowTitle("Minecraft Log")
            self.dialog.show()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))


app = QApplication(sys.argv)
window = MPDB()
window.initUI()
window.show()
sys.exit(app.exec_())
