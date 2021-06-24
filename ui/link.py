from PyQt5.QtWidgets import QLabel


def init(cls, text, pos):
    text = f"<a href={text}>{text}</a>"
    cls.link = QLabel(text, cls)
    cls.link.move(0, pos)
    cls.link.resize(len(text) * 8, cls.link.height())
    cls.link.setOpenExternalLinks(True)