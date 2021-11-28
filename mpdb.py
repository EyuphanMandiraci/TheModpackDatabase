from sys import exit as sys_exit
from sys import argv
from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QCursor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from time import perf_counter
import data
import web_request
from get_ram import get_ram
import funcs
from ui import modpack_selector, ram_selector, username_selector, discord_image, run_button, run_minecraft_info, \
    forge_selector, progress_bar
from webbrowser import open as wb_open
from mail import send_email
from requests import get
from json import loads

run_timer = perf_counter()


class MPDB(QMainWindow):

    rams: List[str]
    mp_names: List[str]
    data: dict
    selected_mp: str
    try:
        def __init__(self):
            super().__init__()
            # self.resize(1000, 600)
            # progress_bar.init(self)


        def initUI(self):

            self.mp_names = web_request.get_data("https://mpdb.xyz/api/modpack.php")
            self.rams = []
            self.data = {}
            self.selected_mp = ""
            self.data = {"downloaded": []}
            if not data.check_path("data.txt"):
                data.set_data("data.txt", self.data)
            else:
                self.data = data.get_data("data.txt")
                if len(self.data["downloaded"]) != 0:
                    pass

            for ram in range(get_ram() - 1, 0, -1):
                self.rams.append(str(ram) + " GB")


            self.setWindowTitle("TheModpackDatabase")
            self.resize(1000, 600)
            self.setStyleSheet("background:rgba(54,57,63,255)")
            self.setMinimumSize(839, 438)
            self.setMouseTracking(True)
            funcs.center(self)
            modpack_selector.init(self, self.data["downloaded"], self.change_button_text)
            ram_selector.init(self, self.rams)
            username_selector.init(self)
            discord_image.init(self, "https://mpdb.xyz/discord.png")
            run_button.init(self, f"RUN {modpack_selector.currentText(self)}", clicked_connect=self.start_runner)
            self.run_button.resize(len(self.run_button.text()) * 8, self.run_button.height())
            run_minecraft_info.init(self)
            forge_selector.init(self, 0)
            # progress_bar.init(self)
            # print(self.progress_bar)

            if len(self.data["downloaded"]) != 0:
                self.run_button.setEnabled(True)

            self.selected_mp = modpack_selector.currentText(self)

            funcs.mp_names_loop(self, self.mp_names, self.start_downloader)
            funcs.hide_download(self, self.data)



        def start_downloader(self):
            funcs.start_download_worker(self, self.sender().objectName(), self.data)

        def change_button_text(self, value):
            funcs.change_button_text(self, value)

        def mouseMoveEvent(self, event):
            if event.x() <= 64 and event.y() <= 64:
                self.setCursor(QCursor(Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

        def mousePressEvent(self, event):
            if event.buttons() == Qt.LeftButton:
                if event.x() <= 64 and event.y() <= 64:
                    wb_open("https://discord.gg/frWGTqhFbn")

        def resizeEvent(self, event):
            self.run_button.move(self.width() - self.run_button.width(), 0)
            self.run_minecraft_info.move(self.width() - self.run_minecraft_info.width(), 30)
            self.username_selector.move(self.width() - self.run_button.width() - self.username_selector.width(), 0)

        def start_runner(self):
            self.run_button.setEnabled(False)
            info = loads(get("https://mpdb.xyz/api/modpack.php?name=" + self.modpack_selector.currentText()).text)
            funcs.start_run_worker(info["mp_version"], info["mp_forge"], info["mp_name"], self.username_selector.text(),
                                   self.ram_selector.currentText(), self)

        def start_run_worker(self, mc_version, forge_version, mp_name):
            self.run = RunThread(mc_version=mc_version, forge_version=forge_version, mp_name=mp_name)
            self.run.start()
            self.run.any_signal.connect(self.stop_run_worker)


        def stop_run_worker(self):
            self.run_button.setEnabled(True)
            self.run.stop()

        def changeValue(self, value):
            progress_bar.init(self)
            self.progress_bar.setValue(value)





    except Exception as e:
        print(e)


class RunThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, mc_version="", forge_version="", mp_name=""):
        super(RunThread, self).__init__(parent)
        self.mc_version = mc_version
        self.forge_version = forge_version
        self.mp_name = mp_name


    def run(self):
        mpdb = MPDB()
        print(f"Running {self.forge_version} for {self.mc_version}")
        link = f"https://mpdb.xyz/forge/{self.mc_version.replace('.','-')}/{self.forge_version}.zip"
        file_name = f"{self.forge_version}.zip"
        with open(file_name, "wb") as f:
            print(f"Downloading {file_name}")
            r = get(link, stream=True)
            total_length = r.headers.get("content-length")
            if total_length is None:
                print(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    mpdb.changeValue(done)
                    print("\r" + str(done))

        self.any_signal.emit()

    def stop(self):
        print("Stopping")
        self.wait()


if __name__ == "__main__":
    app = QApplication(argv)
    mpdb = MPDB()
    mpdb.initUI()
    run_timer = perf_counter() - run_timer
    print(run_timer)
    mpdb.show()
    sys_exit(app.exec_())
