from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from config.settings import TRAY_ICON_PATH

class PetTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(TRAY_ICON_PATH))
        self.setToolTip("单宠物桌宠 - 拖拽文件&碰撞")

        self.menu = QMenu()
        self.show_action = QAction("显示宠物", self, triggered=self.on_show_pet)
        self.hide_action = QAction("隐藏宠物", self, triggered=self.on_hide_pet)
        self.exit_action = QAction("退出", self, triggered=self.on_exit)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)

        self.setContextMenu(self.menu)
        self.show()

        self.show_callback = None
        self.hide_callback = None
        self.exit_callback = None

    def on_show_pet(self):
        if self.show_callback:
            self.show_callback()

    def on_hide_pet(self):
        if self.hide_callback:
            self.hide_callback()

    def on_exit(self):
        if self.exit_callback:
            self.exit_callback()
