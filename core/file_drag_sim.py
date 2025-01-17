from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from config.settings import FILE_ICON_PATH

class FileDragSim(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        pix = QPixmap(FILE_ICON_PATH)
        if not pix.isNull():
            pix = pix.scaled(32,32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(pix)
        self.hide()

    def show_near_pet(self, x, y):
        self.move(x+40, y+40)
        self.show()

    def reset_icon(self):
        self.hide()
