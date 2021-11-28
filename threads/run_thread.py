import subprocess
import time
import tempfile
import random
import threading

import minecraft_launcher_lib.forge
from PyQt5 import QtCore
from sys import stdout

from minecraft_launcher_lib.natives import extract_natives_file, get_natives
from minecraft_launcher_lib.install import install_libraries
from requests import get
from minecraft_launcher_lib import forge, install
from minecraft_launcher_lib.forge import extract_file
from minecraft_launcher_lib.helper import *
from minecraft_launcher_lib.exceptions import *
from minecraft_launcher_lib.runtime import *
from minecraft_launcher_lib.command import *
from .forge_thread import ForgeThread
import copy


def dict_chunkify(input_dict, max_limit):
    chunks = []
    curr_dict = {}
    for k, v in input_dict.items():
        if len(curr_dict.keys()) < max_limit:
            curr_dict.update({k: v})
        else:
            chunks.append(copy.deepcopy(curr_dict))
            curr_dict = {k: v}
    # update last curr_dict
    chunks.append(curr_dict)
    return chunks

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]


def install_forge_libs(data, path, callback):
    print("Forge Libs Başladı")
    callback.get("setMax", empty)(len(data["libraries"]))
    print("DATA: ")
    lib_data1 = chunkify(data["libraries"], 2)[0]
    lib_data2 = chunkify(data["libraries"], 2)[1]
    def lib1():
        print("lib1 start")
        for count, i in enumerate(lib_data1):
            # Check, if the rules allow this lib for the current system
            if not parse_rule_list(i, "rules", {}):
                continue
            # Turn the name into a path
            currentPath = os.path.join(path, "libraries")
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
                download_file(downloadUrl, os.path.join(currentPath, jarFilename), callback)
            except:
                pass
            if "downloads" not in i:
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(path, "versions", data["id"], "natives"), i["extract"])
                continue
            if "artifact" in i["downloads"]:
                download_file(i["downloads"]["artifact"]["url"], os.path.join(currentPath, jarFilename), callback,
                              sha1=i["downloads"]["artifact"]["sha1"])
            if native != "":
                download_file(i["downloads"]["classifiers"][native]["url"],
                              os.path.join(currentPath, jarFilenameNative),
                              callback, sha1=i["downloads"]["classifiers"][native]["sha1"])
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(path, "versions", data["id"], "natives"), i["extract"])
            callback.get("setProgress", empty)(count)
            print("lib1")
        print("lib 1 bitti")

    def lib2():
        print("lib2 start")
        for count, i in enumerate(lib_data2):
            # Check, if the rules allow this lib for the current system
            if not parse_rule_list(i, "rules", {}):
                continue
            # Turn the name into a path
            currentPath = os.path.join(path, "libraries")
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
                download_file(downloadUrl, os.path.join(currentPath, jarFilename), callback)
            except:
                pass
            if "downloads" not in i:
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(path, "versions", data["id"], "natives"), i["extract"])
                continue
            if "artifact" in i["downloads"]:
                download_file(i["downloads"]["artifact"]["url"], os.path.join(currentPath, jarFilename), callback,
                              sha1=i["downloads"]["artifact"]["sha1"])
            if native != "":
                download_file(i["downloads"]["classifiers"][native]["url"],
                              os.path.join(currentPath, jarFilenameNative),
                              callback, sha1=i["downloads"]["classifiers"][native]["sha1"])
                if "extract" in i:
                    extract_natives_file(os.path.join(currentPath, jarFilenameNative),
                                         os.path.join(path, "versions", data["id"], "natives"), i["extract"])
            callback.get("setProgress", empty)(count)
            print("lib2")
        print("lib 2 bitti")
    lib1t = threading.Thread(target=lib1)
    lib2t = threading.Thread(target=lib2)
    lib1t.start()
    lib2t.start()
    lib1t.join()
    lib2t.join()
    print("Forge Libs Bitti")

def install_assets(data, path, callback, index, parse_count):
    print("ASSET INDEX " + str(index))
    if "assetIndex" not in data:
        return
    # Download all assets
    download_file(data["assetIndex"]["url"], os.path.join(path, "assets", "indexes", data["assets"] + ".json"), callback, sha1=data["assetIndex"]["sha1"])
    with open(os.path.join(path, "assets", "indexes", data["assets"] + ".json")) as f:
        assets_data = json.load(f)
    assets_data["objects"] = dict_chunkify(assets_data["objects"], len(assets_data["objects"])/parse_count)[index]
    callback.get("setMax", empty)(len(assets_data["objects"]))
    count = 0
    for key, value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"], os.path.join(path, "assets", "objects", value["hash"][:2], value["hash"]), callback, sha1=value["hash"])
        count += 1
        print(index)
        callback.get("setProgress", empty)(count)

def do_version_install(versionid, path, callback, url=None):
    if url:
        download_file(url, os.path.join(path, "versions", versionid, versionid + ".json"), callback)
    with open(os.path.join(path, "versions", versionid, versionid + ".json")) as f:
        versiondata = json.load(f)
        # For Forge
    if "inheritsFrom" in versiondata:
        versiondata = inherit_json(versiondata, path)
    print("MC libs")
    install_libraries(versiondata, path, callback)
    print("Version Data: ")
    print(versiondata)
    print("MC libs bitti")
    print("Assets Başladı")
    t1 = threading.Thread(target=install_assets, args=(versiondata, path, callback, 0, 5))
    t2 = threading.Thread(target=install_assets, args=(versiondata, path, callback, 1, 5))
    t3 = threading.Thread(target=install_assets, args=(versiondata, path, callback, 2, 5))
    t4 = threading.Thread(target=install_assets, args=(versiondata, path, callback, 3, 5))
    t5 = threading.Thread(target=install_assets, args=(versiondata, path, callback, 4, 5))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    print("Assets Bitti")
    # Download logging config
    if "logging" in versiondata:
        if len(versiondata["logging"]) != 0:
            logger_file = os.path.join(path, "assets", "log_configs", versiondata["logging"]["client"]["file"]["id"])
            download_file(versiondata["logging"]["client"]["file"]["url"], logger_file, callback,
                          sha1=versiondata["logging"]["client"]["file"]["sha1"])
    # Download minecraft.jar
    if "downloads" in versiondata:
        download_file(versiondata["downloads"]["client"]["url"],
                      os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"), callback,
                      sha1=versiondata["downloads"]["client"]["sha1"])
    # Need to copy jar for old forge versions
    if not os.path.isfile(os.path.join(path, "versions", versiondata["id"],
                                       versiondata["id"] + ".jar")) and "inheritsFrom" in versiondata:
        inheritsFrom = versiondata["inheritsFrom"]
        shutil.copyfile(os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"),
                        os.path.join(path, "versions", inheritsFrom, inheritsFrom + ".jar"))
    # Install java runtime if needed
    if "javaVersion" in versiondata:
        callback.get("setStatus", empty)("Install java runtime")
        install_jvm_runtime(versiondata["javaVersion"]["component"], path, callback=callback)


def install_mc(versionid, minecraft_directory, callback=None):
    """
      Install a Minecraft Version. Fore more Information take a look at the documentation"
      """
    if isinstance(minecraft_directory, os.PathLike):
        minecraft_directory = str(minecraft_directory)
    if callback is None:
        callback = {}
    if os.path.isfile(os.path.join(minecraft_directory, "versions", versionid, f"{versionid}.json")):
        do_version_install(versionid, minecraft_directory, callback)
        return
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json",
                                headers={"user-agent": get_user_agent()}).json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(versionid, minecraft_directory, callback, url=i["url"])
            return
    raise VersionNotFound(versionid)


def install_forge(versionid, path, callback=None):
    if callback is None:
        callback = {}
    FORGE_DOWNLOAD_URL = \
        "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    temp_file_path = os.path.join(tempfile.gettempdir(), "forge-installer-" + str(random.randrange(1, 100000)) + ".tmp")
    if not download_file(FORGE_DOWNLOAD_URL.format(version=versionid), temp_file_path, callback):
        raise VersionNotFound(versionid)
    zf = zipfile.ZipFile(temp_file_path, "r")
    # Read the install_profile.json
    with zf.open("install_profile.json", "r") as f:
        version_content = f.read()
    version_data = json.loads(version_content)
    forge_version_id = version_data["version"]
    t_mc = threading.Thread(target=install_mc,
                            args=(version_data["minecraft"], path, callback,))
    t_libs = ForgeThread(version_data, path, callback)
    t_mc.start()
    print("MC Başladı")
    t_libs.start()
    t_libs.any_signal.connect(t_libs.stop)
    t_mc.join()
    print("MC Join")
    version_json_path = os.path.join(path, "versions", forge_version_id, forge_version_id + ".json")
    extract_file(zf, "version.json", version_json_path)
    # Extract forge libs from the installer
    forge_lib_path = os.path.join(path, "libraries", "net", "minecraftforge", "forge", versionid)
    try:
        print("Extract file 1 başladı")
        extract_file(zf, "maven/net/minecraftforge/forge/{version}/forge-{version}.jar".format(version=versionid),
                     os.path.join(forge_lib_path, "forge-" + versionid + ".jar"))
        print("Extract file 1 bitti")
        print("Extract file 2 başladı")
        extract_file(zf,
                     "maven/net/minecraftforge/forge/{version}/forge-{version}-universal.jar".format(version=versionid),
                     os.path.join(forge_lib_path, "forge-" + versionid + "-universal.jar"))
        print("Extract file 1 bitti")
    except KeyError:
        pass
    # Extract the client.lzma
    lzma_path = os.path.join(tempfile.gettempdir(), "lzma-" + str(random.randrange(1, 100000)) + ".tmp")
    print("LZMA Başladı")
    extract_file(zf, "data/client.lzma", lzma_path)
    print("LZMA Bitti")
    zf.close()
    # Install the rest with the vanilla function
    print("MC Tekrar Başladı")
    install.install_minecraft_version(forge_version_id, path, callback=callback)
    print("MC Bitti")
    # Run the processors
    print("Forge Processors")
    forge.forge_processors(version_data, path, lzma_path, temp_file_path, callback)
    # Delete the temporary files
    os.remove(temp_file_path)
    os.remove(lzma_path)


class RunThread(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None, mc_version="", forge_version="", mp_name="", username="MPDB_User", ram="2 GB"):
        super(RunThread, self).__init__(parent)
        self.mc_version = mc_version
        self.forge_version = forge_version
        self.mp_name = mp_name
        self.username = username
        self.ram = ram
        print(username)

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
        # Print New Line on Complete
        if iteration == total:
            print()

    def maximum(self, max_value, value):
        max_value[0] = value

    def run(self):
        print(f"Running {self.forge_version} for {self.mc_version}")
        max_value = [0]

        callback = {
            "setStatus": lambda text: print(text),
            "setProgress": lambda value: self.printProgressBar(value, max_value[0]),
            "setMax": lambda value: self.maximum(max_value, value)
        }
        s = time.perf_counter()
        install_forge(f"{self.mc_version}-{self.forge_version}", path=self.mp_name, callback=callback)
        print("Forge inme süresi: " + str(time.perf_counter() - s))
        options = {
            "username": self.username,
            "jvmArguments": [f"-Xmx{self.ram.replace(' GB', 'G')}"]
        }
        forge_ver = self.mc_version + "-forge-" + self.forge_version
        print(forge_ver)
        minecraft_command = get_minecraft_command(forge_ver, self.mp_name, options)
        subprocess.call(minecraft_command)
        self.any_signal.emit()

    def stop(self):
        print("Stopping")
        self.wait()
