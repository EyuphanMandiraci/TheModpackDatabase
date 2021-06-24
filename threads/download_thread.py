from PyQt5 import QtCore
import funcs
import web_request
from pathlib import Path


class DownloadThread(QtCore.QThread):
    name: str
    author: str
    version: str
    any_signal = QtCore.pyqtSignal()
    try:


        def __init__(self, mp_name="", data="", parent=None):
            super(DownloadThread, self).__init__(parent)
            self.mp_name = mp_name
            self.data = data

        def run(self):
            print("Downloading ModPack")
            r = web_request.get_data(f"https://mpdb.xyz/get_data.php?data=true&from=name&name={self.mp_name}")
            self.name = r["name"]
            self.author = r["author"]
            self.version = r["version"]
            Path(self.name).mkdir(parents=True, exist_ok=True)
            funcs.download_modpack(self.name, self.author, self.data)
            self.any_signal.emit()

        def stop(self):
            print("Download Complete!")
            self.wait()

    except Exception as e:
        print(e)
