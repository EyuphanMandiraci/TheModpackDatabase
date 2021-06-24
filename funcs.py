from PyQt5.QtWidgets import QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import Qt
from ui import link
from json import dump


def none_test():
    pass


def center(cls):
    qr = cls.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    cls.move(qr.topLeft())


def mp_names_loop(cls, mp_names, clicked_connect=none_test):
    pos = 130
    width = len(max(mp_names, key=len)) * 8
    for i in mp_names:
        cls.mp_label = QLabel(i, cls)
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
        cls.mp_button.setObjectName(i)
        pos += 30
    link.init(cls, "https://mpdb.xyz", pos+30)


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


