from PyQt5.QtWidgets import QLabel


class ModpackText(QLabel):
    def __init__(self, text, *args):
        super(ModpackText, self).__init__(text, *args)
        