from PyQt5.QtWidgets import QMainWindow, QLabel


class CreditsWindow(QMainWindow):
    def __init__(self):
        super(CreditsWindow, self).__init__()
        self.setFixedSize(500, 600)
        self.coder = QLabel("Coder: TheKralGame", self)
        self.coder.resize(500, 30)
        self.screenshot_credit = QLabel('<a href="https://www.flaticon.com/free-icons/image" title="image '
                                        'icons">rsetiawan - Screenshot Icon</a>', self)
        self.screenshot_credit.setOpenExternalLinks(True)
        self.screenshot_credit.move(0, 30)
        self.screenshot_credit.resize(500, 30)
