from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from ui import modpack_selector, modpack_text, modpack_download_button
from requests import get

from ui.modpack_download_button import ModpackDlButton
from ui.modpack_text import ModpackText


class MPDB(QMainWindow):
    mp_dl_button: ModpackDlButton
    mp_text: ModpackText

    def __init__(self):
        super(MPDB, self).__init__()
        self.resize(QSize(1000, 600))
        self.setWindowTitle("TheModpackDatabase")

    def initUI(self):
        mp_selector = modpack_selector.ModpackSelector(self)
        mp_selector.resize(QSize(200, 50))
        mp_selector.move(QPoint(0, 0))
        mp_selector.addItem("CrazyCraft")
        mp_selector.addItem("Hexxit")
        self.modpacksloop()

    def modpacksloop(self):
        modpacks = get("https://mpdb.xyz/api/modpack.php").json()
        count = 50
        for i in modpacks:
            self.mp_text = modpack_text.ModpackText(i["mp_name"], self)
            self.mp_text.move(0, count)
            self.mp_text.setToolTip(i["mp_author"])
            self.mp_dl_button = modpack_download_button.ModpackDlButton("Download", self)
            self.mp_dl_button.move(100, count)
            count += self.mp_text.height()






app = QApplication(sys.argv)
window = MPDB()
window.initUI()
window.show()
sys.exit(app.exec_())