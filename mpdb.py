from sys import exit as sys_exit
from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QMouseEvent, QCursor
from PyQt5.QtCore import Qt
from time import perf_counter
import data
import web_request
from get_ram import get_ram
import funcs
from ui import modpack_selector, ram_selector, username_selector, discord_image, run_button, run_minecraft_info
from webbrowser import open as wb_open



class MPDB(QMainWindow):
    try:
        def __init__(self):
            super().__init__()
            self.mp_names = web_request.get_data("https://mpdb.xyz/get_data.php")
            self.rams = []
            self.data = {}
            self.selected_mp = ""

        def initUI(self):
            run_timer = perf_counter()
            self.data = {"downloaded": []}
            if not data.check_path("data.txt"):
                data.set_data("data.txt", self.data)
            else:
                self.data = data.get_data("data.txt")
                if len(self.data["downloaded"]) != 0:
                    # TODO: Buraya run butonunu disable etmeyi ekle
                    pass

            for ram in range(get_ram()-1, 0, -1):
                self.rams.append(str(ram) + " GB")

            self.resize(1000, 600)
            self.setWindowTitle("TheModpackDatabase")
            self.setStyleSheet("background:rgba(54,57,63,255)")
            self.setMinimumSize(839, 438)
            self.setMouseTracking(True)
            funcs.center(self)
            modpack_selector.init(self, self.data["downloaded"], self.change_button_text)
            ram_selector.init(self, self.rams)
            username_selector.init(self)
            discord_image.init(self, "https://mpdb.xyz/discord.png")
            run_button.init(self, f"RUN {modpack_selector.currentText(self)}")
            run_minecraft_info.init(self)
            self.selected_mp = modpack_selector.currentText(self)

            funcs.mp_names_loop(self, self.mp_names)
            funcs.hide_download(self, self.data)

            run_timer = perf_counter() - run_timer
            print(run_timer)


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
                    wb_open("https://discord.gg/frWGTqhFbn", new=0, autoraise=True)

        def resizeEvent(self, event):
            self.run_button.move(self.width() - self.run_button.width(), 0)
            self.run_minecraft_info.move(self.width() - self.run_minecraft_info.width(), 30)
            self.username_selector.move(self.width() - self.run_button.width() - self.username_selector.width(), 0)



    except Exception as e:
        print(e)


if __name__ == "__main__":
    app = QApplication(argv)
    mpdb = MPDB()
    mpdb.initUI()
    mpdb.show()
    sys_exit(app.exec_())

