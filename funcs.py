import os

from PyQt5.QtWidgets import QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
import web_request
from ui import link
from json import dump, loads
from wget import download
from zipfile import ZipFile
from os import listdir, remove
from shutil import move, rmtree
from pathlib import Path
from random import choice
from threads import download_thread, run_thread
from requests import get


def none_test():
    pass


def center(cls):
    qr = cls.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    cls.move(qr.topLeft())


def mp_names_loop(cls, mp_names, clicked_connect=none_test):
    pos = 130
    names = []
    for i in mp_names:
        names.append(i["mp_name"])
    width = len(max(names, key=len)) * 8
    for i in mp_names:
        cls.mp_label = QLabel(i["mp_name"], cls)
        cls.mp_label.move(0, pos)
        cls.mp_label.resize(width, cls.mp_label.height())
        cls.mp_label.setAlignment(Qt.AlignLeft)
        pos += 30
    pos = 130
    for i in mp_names:
        cls.mp_button = QPushButton("Download", cls)
        cls.mp_button.move(width, pos)
        cls.mp_button.setStyleSheet("background:rgba(185,187,190,255)")
        cls.mp_button.clicked.connect(clicked_connect)
        cls.mp_button.setObjectName(i["mp_name"])
        pos += 30
    link.init(cls, "https://mpdb.xyz", pos + 30)


def hide_download(cls, downloaded):
    pass
    for i in downloaded["downloaded"]:
        button = cls.findChild(QPushButton, i)
        if button is not None:
            button.hide()
        elif button is None:
            downloaded["downloaded"].remove(i)


def change_button_text(cls, value):
    cls.run_button.setText(f"Run {value}")
    cls.selected_mp = value
    cls.forge_selector.clear()
    info = loads(get(f"https://mpdb.xyz/api/modpack.php?name={value}").text)
    cls.forge_selector.addItems(get_forges(info["mp_version"]))
    cls.run_button.resize(len("Run " + value) * 8, cls.run_button.height())
    cls.username_selector.move(cls.width() - cls.run_button.width() - cls.username_selector.width(), 0)
    cls.run_button.move(cls.width() - cls.run_button.width(), 0)



def download_modpack(name, author, data):
    global display_name, download_url
    print(f"Downloading {name} by {author}!")
    download(f"http://185.255.94.159/modpacks/{author}/{name}.zip")
    os.rename(f"{name}.zip", f"{author}_{name}.zip")
    zip_path = f"{author}_{name}.zip"
    if name not in data["downloaded"]:
        data["downloaded"].append(name)
        dosya = open("data.txt", "w")
        dump(data, dosya, ensure_ascii=False, indent=4, sort_keys=True)
        dosya.close()
    zip = ZipFile(zip_path, "r")
    all_files = zip.namelist()
    if "modlist.html" in all_files:
        for i in all_files:
            if "overrides" in i:
                zip.extract(i, name)
        for i in listdir(f"{name}/overrides"):
            move(f"{name}/overrides/{i}", f"{name}")
        manifest = loads(zip.read("manifest.json"))
        Path(f"{name}/mods").mkdir(parents=True, exist_ok=True)

        for id in manifest["files"]:
            pid = id["projectID"]
            fid = id["fileID"]
            l = ["cursemeta", "curse_nicky"]
            choosed = choice(l)
            if choosed == "cursemeta":
                r = web_request.get_data(f"https://cursemeta.dries007.net/{pid}/{fid}.json")
                display_name = r["DisplayName"]
                download_url = r["DownloadURL"]
            elif choosed == "curse_nicky":
                r = web_request.get_data(f"https://curse.nikky.moe/api/addon/{pid}/file/{fid}")
                display_name = r["displayName"]
                download_url = r["downloadUrl"]
            print(f"Downloading {display_name}")
            download(download_url, f"{name}/mods")
        rmtree(f"{name}/overrides")
        zip.close()
        remove(f"{author}_{name}.zip")

    else:
        zip.extractall(name)
        zip.close()
        remove(f"{author}_{name}.zip")


# Thread Runners and Stoppers

def start_download_worker(cls, mp_name, data):
    global thread
    global cl
    global modpack_name
    modpack_name = mp_name
    cl = cls
    thread = download_thread.DownloadThread(parent=None, mp_name=mp_name, data=data)
    thread.start()
    cls.run_minecraft_info.setText(f"Downloading {mp_name}")
    cls.run_minecraft_info.resize(len(f"Downloading {mp_name}") * 8, cls.run_minecraft_info.height())
    for i in cls.mp_names:
        b = cls.findChild(QPushButton, i["mp_name"])
        b.setEnabled(False)
    cls.run_button.setEnabled(False)
    cls.modpack_selector.setEnabled(False)
    cls.ram_selector.setEnabled(False)
    cls.username_selector.setEnabled(False)
    thread.any_signal.connect(stop_download_worker)


def stop_download_worker():
    thread.stop()
    cl.run_minecraft_info.setText("")
    print(cl.mp_names)
    for i in cl.mp_names:
        b = cl.findChild(QPushButton, i["mp_name"])
        b.setEnabled(True)
    b = cl.findChild(QPushButton, modpack_name)
    b.hide()
    cl.run_button.setEnabled(True)
    cl.modpack_selector.setEnabled(True)
    cl.ram_selector.setEnabled(True)
    cl.username_selector.setEnabled(True)
    cl.modpack_selector.addItem(modpack_name)
    cl.modpack_selector.adjustSize()


forges = loads(get("https://raw.githubusercontent.com/MultiMC/meta-upstream/master/forge/maven-metadata.json").text)


def get_forges(version=None):
    if version is not None:
        return forges[version]


def start_run_worker(mc_version, forge_version, mp_name, username, ram, cls):
    global run
    if username == "":
        run = run_thread.RunThread(mc_version=mc_version, forge_version=forge_version, mp_name=mp_name, ram=ram)
    else:
        run = run_thread.RunThread(mc_version=mc_version, forge_version=forge_version, mp_name=mp_name,
                                   username=username, ram=ram)
    run.start()
    run.any_signal.connect(lambda cls=cls: stop_run_worker(cls))

def stop_run_worker(cls):
    cls.run_button.setEnabled(True)
    run.stop()


def download_file(url, path=""):
    with open(path, "wb") as f:
        r = get(url, stream=True)
        total_length = r.headers.get("content-length")
        if total_length is None:
            print(r.content)
        else:
            total_length = int(total_length)
            for data in r.iter_content(chunk_size=4096):
                f.write(data)




