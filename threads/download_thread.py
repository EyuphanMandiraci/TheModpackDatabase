from PyQt5 import QtCore
from wget import download


class DownloadThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, url, **kwargs):
        super(DownloadThread, self).__init__(**kwargs)
        self.url = url

    def run(self) -> None:
        download(self.url)
        self.any_signal.emit()

    def stop(self):
        print("Download Complete!")
        self.wait()