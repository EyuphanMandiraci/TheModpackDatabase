from PyQt5 import QtCore
from wget import download
import zipfile
from pathlib import Path
import json
from os import listdir, remove
from shutil import move, rmtree
from requests import get


class DownloadThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, url, mp_info, **kwargs):
        super(DownloadThread, self).__init__(**kwargs)
        self.url = url
        self.mp_info = mp_info
        self.window = kwargs["parent"]

    def run(self) -> None:
        for i in self.window.mp_buttons:
            i.setEnabled(False)
        print("Download Started")
        self.window.status.setText(f"Downloading {self.mp_info['mp_name']}")
        download(self.url)
        print(f"Download Completed! URL: {self.url}")
        print("Installing Modpack")
        mp_zip = zipfile.ZipFile(self.mp_info["mp_file"], "r")
        Path(self.mp_info["mp_name"] + "/mods").mkdir(parents=True, exist_ok=True)
        files = mp_zip.namelist()
        isCurseforge = False
        if "manifest.json" in files:
            isCurseforge = True
        if isCurseforge:
            manifest = json.loads(mp_zip.read("manifest.json"))
            allmods = manifest["files"]
            for mod in allmods:
                mod_info = get(f"https://cursemeta.dries007.net/{mod['projectID']}/{mod['fileID']}.json").json()
                self.window.status.setText(f"Downloading {mod_info['DisplayName']}")
                print(f"Downloading {mod_info['DisplayName']}")
                download(mod_info["DownloadURL"], out=f"{self.mp_info['mp_name']}/mods")
            for file in files:
                if "overrides" in file:
                    mp_zip.extract(file, self.mp_info["mp_name"])
            for file in listdir(f"{self.mp_info['mp_name']}/overrides"):
                move(f"{self.mp_info['mp_name']}/overrides/{file}", f"{self.mp_info['mp_name']}/{file}")
            rmtree(f"{self.mp_info['mp_name']}/overrides")
        else:
            mp_zip.extractall(self.mp_info["mp_name"])
        mp_zip.close()
        remove(self.mp_info["mp_file"])
        self.any_signal.emit()

    def stop(self):
        print("Modpack Installed")
        self.window.status.setText("")
        for i in self.window.mp_buttons:
            i.setEnabled(True)
        self.wait()

