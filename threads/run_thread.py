import traceback

import wget
from PyQt5 import QtCore
from subprocess import Popen, PIPE
import minecraft_launcher_lib as mll
from pathlib import Path
from shutil import copyfile
from os import remove, system, path
import platform

from utils import log


class RunThread(QtCore.QThread):
    run_started = QtCore.pyqtSignal()
    running = QtCore.pyqtSignal()
    logging = QtCore.pyqtSignal(str)
    stopped = QtCore.pyqtSignal()

    def __init__(self, mp_info, **kwargs):
        super(RunThread, self).__init__(**kwargs)
        self.c = None
        self.mp_info = mp_info
        self.window = kwargs["parent"]
        self.mp_forge = mp_info["mp_version"] + "-forge-" + mp_info["mp_forge"]

    def run(self) -> None:
        try:
            username = self.window.user_selector.text()
            if username == "":
                username = "MPDB"
            if len(username) < 3:
                username += "___"

            if self.window.skinpath is not None:
                skin_mod_url = "https://media.forgecdn.net/files/3621/647/CustomSkinLoader_ForgeLegacy-14.13-SNAPSHOT" \
                               "-313.jar"
                wget.download(skin_mod_url, out=f"{self.mp_info['mp_name']}/mods")
                Path(f"{self.window.instancepath}/{self.mp_info['mp_name']}/CustomSkinLoader/LocalSkin/skins").mkdir(exist_ok=True, parents=True)
                try:
                    remove(f"{self.window.instancepath}/{self.mp_info['mp_name']}/CustomSkinLoader/CustomSkinLoader.json")
                except Exception as e:
                    print(e)
                wget.download("https://mpdb.xyz/static/CustomSkinLoader.json", out=f"{self.window.instancepath}/"
                                                                                   f"{self.mp_info['mp_name']}"
                                                                                   f"/CustomSkinLoader")
                try:
                    remove(path.join(f"{self.window.instancepath}/{self.mp_info['mp_name']}", "CustomSkinLoader",
                                     "LocalSkin", "skins",
                                     f"{username}.png"))
                except Exception as e:
                    print(e)
                copyfile(self.window.skinpath, f"{self.window.instancepath}/{self.mp_info['mp_name']}"
                                               f"/CustomSkinLoader/LocalSkin/skins/{username}.png")
            else:
                try:
                    remove(path.join(f"{self.window.instancepath}/{self.mp_info['mp_name']}", "CustomSkinLoader",
                                     "LocalSkin", "skins",
                                     f"{username}.png"))
                except Exception as e:
                    print(e)
            ram = int(self.window.ram_selector.currentText().replace(" GB", "")) * 1024
            options = {
                "username": username,
                "jvmArguments": ["-Xms512M", f"-Xmx{ram}M"]
            }
            print("İnen Sürümler:", mll.utils.get_installed_versions(self.window.instancepath + "/" + self.mp_info["mp_name"]))
            command = mll.command.get_minecraft_command(self.mp_forge,
                                                        self.window.instancepath + "/" + self.mp_info["mp_name"],
                                                        options)
            if platform.system() == "Linux":
                system(f'chmod +x \"{self.window.instancepath + "/" + self.mp_info["mp_name"]}/runtime/jre-legacy/linux/jre-legacy/bin/java\"')
            self.c = Popen(command, stdout=PIPE)
            self.run_started.emit()
            while True:
                output = self.c.stdout.readline()
                if not output:
                    break
                self.logging.emit(output.strip().decode("utf-8"))
                self.running.emit()
            self.stopped.emit()
        except Exception as e:
            log.error(str(traceback.format_tb(e.__traceback__)) + f" \nError: {e}")

    def killMinecraft(self):
        try:
            self.c.kill()
            self.stopped.emit()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def stop(self):
        self.wait()
