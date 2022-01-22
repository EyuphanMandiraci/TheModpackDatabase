from PyQt5.QtWidgets import QPushButton


class ModpackDlButton(QPushButton):
    def __init__(self, text, mp_name, *args):
        super(ModpackDlButton, self).__init__(text, *args)
        self.setObjectName(mp_name)
