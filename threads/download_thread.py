from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    try:
        any_signal = pyqtSignal()

        def __init__(self, mp_name, download_list, parent=None):
            super(DownloadThread, self).__init__(parent)
            self.mp_name = mp_name
            self.download_list = download_list

        def run(self):
            print("Downloading ModPack")




    except Exception as e:
        print(e)
