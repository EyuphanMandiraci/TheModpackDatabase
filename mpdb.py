# Libraries
from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from ui import modpack_selector, modpack_text, modpack_download_button
from requests import get, HTTPError, ConnectionError
import wget

# UI Components
from ui.modpack_download_button import ModpackDlButton
from ui.modpack_text import ModpackText

# Threads
from threads import download_thread


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
        try:
            modpacks = get("https://mpdb.xyz/api/modpack.php").json()
        except HTTPError as e:
            modpacks = get("https://mpdb.xyz/api/modpack.php", verify=False).json()
        except ConnectionError as e:
            modpacks = get("https://mpdb.xyz/api/modpack.php", verify=False).json()
        count = 50
        for i in modpacks:
            self.mp_text = modpack_text.ModpackText(i["mp_name"], self)
            self.mp_text.move(0, count)
            self.mp_text.setToolTip(i["mp_author"])
            self.mp_dl_button = modpack_download_button.ModpackDlButton("Download", self.mp_text.text(), self)
            self.mp_dl_button.move(100, count)
            self.mp_dl_button.clicked.connect(self.downloadModpack)
            count += self.mp_text.height()

    def downloadModpack(self):
        mp_name = self.sender().objectName()
        mp_info = get(f"https://mpdb.xyz/api/modpack?name={mp_name}").json()[0]
        file_name = mp_info["mp_file"]
        server_info = get(f"https://mpdb.xyz/api/server?server={mp_info['server']}").json()[0]
        dlth = download_thread.DownloadThread(server_info["url"] + file_name, parent=self)
        dlth.any_signal.connect(dlth.stop)
        dlth.start()


app = QApplication(sys.argv)
window = MPDB()
window.initUI()
window.show()
sys.exit(app.exec_())
