from PyQt5 import QtCore
from minecraft_launcher_lib.helper import *
from minecraft_launcher_lib.natives import *


class ForgeThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, libs, path, callback):
        super().__init__()
        self.libs = libs
        self.path = path
        self.callback = callback
        self.callback.get("setMax", empty)(len(self.libs["libraries"]))

    def run(self) -> None:
        print("Yeni libs")
        for count, i in enumerate(self.libs["libraries"]):
            # Check, if the rules allow this lib for the current system
            if not parse_rule_list(i, "rules", {}):
                continue
            # Turn the name into a path
            currentPath = os.path.join(self.path, "libraries")
            if "url" in i:
                if i["url"].endswith("/"):
                    downloadUrl = i["url"][:-1]
                else:
                    downloadUrl = i["url"]
            else:
                downloadUrl = "https://libraries.minecraft.net"
            try:
                libPath, name, version = i["name"].split(":")
            except:
                continue
            for libPart in libPath.split("."):
                currentPath = os.path.join(currentPath, libPart)
                downloadUrl = downloadUrl + "/" + libPart
            try:
                version, fileend = version.split("@")
            except:
                fileend = "jar"
            jarFilename = name + "-" + version + "." + fileend
            downloadUrl = downloadUrl + "/" + name + "/" + version
            currentPath = os.path.join(currentPath, name, version)
            native = get_natives(i)
            # Check if there is a native file
            if native != "":
                jarFilenameNative = name + "-" + version + "-" + native + ".jar"
            jarFilename = name + "-" + version + "." + fileend
            downloadUrl = downloadUrl + "/" + jarFilename
            # Try to download the lib
            try:
                download_file(downloadUrl, os.path.join(currentPath, jarFilename), self.callback)
            except:
                pass
            if "downloads" not in i:
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(self.path, "versions", self.data["id"], "natives"), i["extract"])
                continue
            if "artifact" in i["downloads"]:
                download_file(i["downloads"]["artifact"]["url"], os.path.join(currentPath, jarFilename), self.callback,
                              sha1=i["downloads"]["artifact"]["sha1"])
            if native != "":
                download_file(i["downloads"]["classifiers"][native]["url"],
                              os.path.join(currentPath, jarFilenameNative),
                              self.callback, sha1=i["downloads"]["classifiers"][native]["sha1"])
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(self.path, "versions", self.libs["id"], "natives"), i["extract"])
            self.callback.get("setProgress", empty)(count)
            print("yeni lib1")
        print("yeni lib 1 bitti")
        self.any_signal.emit()

    def stop(self):
        self.wait()
