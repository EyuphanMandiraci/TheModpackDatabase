import os.path
import traceback

from PyQt5 import QtCore
import zipfile
from pathlib import Path
import json
from os import listdir, remove, getcwd
from shutil import move, rmtree, make_archive
from requests import get
from urllib.parse import urlparse
from wget import download
import minecraft_launcher_lib as mll
from subprocess import call
from platform import system

from utils import log


class DownloadThread(QtCore.QThread):
    download_signal = QtCore.pyqtSignal(int, int, int)
    download_completed = QtCore.pyqtSignal(QtCore.QThread)

    def __init__(self, url, mp_info, **kwargs):
        super(DownloadThread, self).__init__(**kwargs)
        self.url = url
        self.mp_info = mp_info
        self.window = kwargs["parent"]

    def run(self) -> None:
        try:
            for i in self.window.mp_buttons:
                i.setEnabled(False)
            if self.mp_info['mp_name'] in listdir(getcwd()):
                rmtree(self.mp_info['mp_name'])
            print("Download Started")
            self.window.status.setText(f"Downloading {self.mp_info['mp_name']}")
            self.download_file(self.url)
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
                self.download_mods(allmods)
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
            print("Modpack Installed")
            print("Minecraft and Forge Installing")
            self.download_minecraft()
            self.window.status.setText("")
            for i in self.window.mp_buttons:
                i.setEnabled(True)
            self.download_completed.emit(self)
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def download_file(self, url, out=""):
        try:
            if out != "":
                out += "/"
            downloaded = 0
            with open(out + os.path.basename(urlparse(url).path), "wb") as f:
                r = get(url, stream=True)
                total_length = r.headers.get("content-length")
                if total_length is None:
                    print(r.content)
                else:
                    total_length = int(total_length)
                    for data in r.iter_content(chunk_size=4096):
                        f.write(data)
                        downloaded += len(data)
                        self.download_signal.emit(downloaded * 100 / total_length, downloaded, total_length)
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def download_mods(self, mods):
        try:
            downloaded = 0
            for mod in mods:
                mod_info = get(f"https://cursemeta.dries007.net/{mod['projectID']}/{mod['fileID']}.json").json()
                try:
                    all_info = get(f"https://addons-ecs.forgesvc.net/api/v2/addon/{mod['projectID']}",
                                   headers={"User-Agent": "TheMPDB"}).json()
                except Exception as e:
                    all_info = {'name': mod_info["DisplayName"]}
                self.window.status.setText(f"Downloading {all_info['name']}")
                print(f"Downloading {all_info['name']} {downloaded * 100 / len(mods)}")
                download(mod_info["DownloadURL"], out=f"{self.mp_info['mp_name']}/mods")
                downloaded += 1
                self.download_signal.emit(downloaded * 100 / len(mods), downloaded, len(mods))
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))

    def download_minecraft(self):
        try:
            Path(f"{str(Path().home())}/.mpdbtemp").mkdir(exist_ok=True, parents=False)
            self.window.status.setText("Downloading Minecraft and Forge! (Progress Bar Not Working In This Part)")
            if f"{self.mp_info['mp_version']}-{self.mp_info['mp_forge']}.zip" in os.listdir(f"{str(Path().home())}/.mpdbtemp"):
                zf = zipfile.ZipFile(f"{str(Path().home())}/.mpdbtemp/{self.mp_info['mp_version']}-{self.mp_info['mp_forge']}.zip", "r")
                zf.extractall(self.mp_info['mp_name'])
                command = mll.command.get_minecraft_command(
                    f"{self.mp_info['mp_version']}-forge-{self.mp_info['mp_forge']}", self.mp_info['mp_name'],
                    mll.utils.generate_test_options())
                os.system(f"chmod +x {self.mp_info['mp_name']}/runtime/jre-legacy/linux/jre-legacy/bin/java")
                call(command)
            else:
                Path("temp").mkdir(exist_ok=True)
                mll.forge.install_forge_version(f"{self.mp_info['mp_version']}-{self.mp_info['mp_forge']}", "temp")
                make_archive(f"{str(Path().home())}/.mpdbtemp/{self.mp_info['mp_version']}-{self.mp_info['mp_forge']}", "zip", "temp")
                zf = zipfile.ZipFile(f"{str(Path().home())}/.mpdbtemp/{self.mp_info['mp_version']}-{self.mp_info['mp_forge']}.zip", "r")
                zf.extractall(self.mp_info['mp_name'])
                rmtree("temp")
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))
