from PyQt5 import QtCore
from minecraft_launcher_lib import forge, command
from subprocess import call


class RunThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, mc_version="", forge_version="", mp_name=""):
        super(RunThread, self).__init__(parent)
        self.mc_version = mc_version
        self.forge_version = forge_version
        self.mp_name = mp_name


    def run(self):
        print(f"Running {self.forge_version} for {self.mc_version}")
        forge_version = forge.find_forge_version(self.mc_version).split("-")[0] + "-forge-" + forge.find_forge_version(self.mc_version).split("-")[1]
        forge.install_forge_version(forge.find_forge_version(self.mc_version), f"{self.mp_name}")
        call(command.get_minecraft_command(forge_version, f"{self.mp_name}", {"username" : "MPDB"}))




