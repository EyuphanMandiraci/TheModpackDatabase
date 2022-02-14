import traceback

from PyQt5.QtWidgets import QComboBox
from psutil import virtual_memory

from utils import log


class RamSelector(QComboBox):
    def __init__(self, *args, **kwargs):
        try:
            super(RamSelector, self).__init__(*args, **kwargs)
            rams = [i + 1 for i in range((((virtual_memory().total // 1024) // 1024) // 1024) - 1)]
            rams = reversed(list(map(str, rams)))
            rams = list(map(lambda orig_string: orig_string + " GB", rams))
            self.addItems(rams)
            self.adjustSize()
        except Exception as e:
            log.error(traceback.format_tb(e.__traceback__))
