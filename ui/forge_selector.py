from PyQt5.QtWidgets import QComboBox
from requests import get
from funcs import get_forges
from json import loads


def init(cls, values):
    cls.forge_selector = QComboBox(cls)
    cls.forge_selector.move(cls.modpack_selector.width(), 70)
    cls.forge_selector.setStyleSheet("background:rgba(185,187,190,255)")
    info = loads(get("https://mpdb.xyz/get_data.php?data=true&from=name&name=" + cls.modpack_selector.currentText()).text)
    if cls.modpack_selector.currentText() != "":
        cls.forge_selector.addItems(get_forges(info["version"]))
    cls.forge_selector.adjustSize()
