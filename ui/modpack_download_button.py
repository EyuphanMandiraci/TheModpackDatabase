from PyQt5.QtWidgets import QPushButton


class ModpackDlButton(QPushButton):
    def __init__(self, text, *args):
        super(ModpackDlButton, self).__init__(text, *args)