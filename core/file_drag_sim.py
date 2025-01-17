# core/file_drag_sim.py

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from config.settings import ASSETS_DIR
import os

class FileDragSim(QLabel):
    """
    仅做视觉模拟：显示一个文件图标，跟随宠物移动/拖拽。
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        icon_path = os.path.join(ASSETS_DIR, "images", "file_icon.png")
        self.pixmap = QPixmap(icon_path)
        self.setPixmap(self.pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.hide()

    def show_near_pet(self, pet_x, pet_y):
        """
        在宠物附近显示图标
        """
        self.move(pet_x + 40, pet_y + 40)
        self.show()

    def reset_icon(self):
        """
        隐藏并回到默认位置
        """
        self.hide()
