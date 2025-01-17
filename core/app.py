from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import datetime
import sys

from config.states import PetState
from core.pet_logic import PetLogic
from core.pet_window import PetWindow
from core.tray_icon import PetTrayIcon
from core.unlock_manager import UnlockManager

class PetApp:
    def __init__(self):
        from PyQt5.QtGui import QGuiApplication
        screen_rect = QGuiApplication.primaryScreen().availableGeometry()
        self.screen_width = screen_rect.width()-50
        self.screen_height = screen_rect.height()-50

        self.logic = PetLogic(self.screen_width, self.screen_height)
        self.unlock_manager = UnlockManager()
        self.window = PetWindow(self.logic, self.unlock_manager)
        self.window.show()

        self.tray = PetTrayIcon()
        self.tray.show_callback = self.show_pet
        self.tray.hide_callback = self.hide_pet
        self.tray.exit_callback = self.exit_app

        # 可加定时器更新(如日夜判断), 这里只演示最小功能
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_loop)
        # self.timer.start(2000)

    def show_pet(self):
        self.window.show()

    def hide_pet(self):
        self.window.hide()

    def exit_app(self):
        self.window.hide()
        self.tray.hide()
        QApplication.quit()

    # def update_loop(self):
    #     # 若要做日夜 或 其他周期更新
    #     pass

def main():
    app = QApplication(sys.argv)
    PetApp()
    sys.exit(app.exec_())
