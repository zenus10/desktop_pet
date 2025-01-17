# core/tray_icon.py

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QInputDialog
from PyQt5.QtGui import QIcon
from config.settings import TRAY_ICON_PATH
from core.focus_timer import FocusTimer
from core.web_climb_sim import WebClimbSim

class PetTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(TRAY_ICON_PATH))
        self.setToolTip("自嘲熊桌宠 - 扩展版")

        self.focus_timer = FocusTimer()
        self.focus_timer.focus_finished.connect(self.on_focus_finished)

        self.web_climb_window = None

        self.menu = QMenu()
        self.show_action = QAction("显示宠物", self, triggered=self.on_show_pets)
        self.hide_action = QAction("隐藏宠物", self, triggered=self.on_hide_pets)
        self.set_city_action = QAction("设置城市(天气)", self, triggered=self.on_set_city)
        self.start_focus_action = QAction("开始专注(番茄钟)", self, triggered=self.on_start_focus)
        self.stop_focus_action = QAction("停止专注", self, triggered=self.on_stop_focus)
        self.open_web_action = QAction("网页爬行演示", self, triggered=self.on_open_web_climb)
        self.exit_action = QAction("退出", self, triggered=self.on_exit)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addSeparator()
        self.menu.addAction(self.set_city_action)
        self.menu.addAction(self.start_focus_action)
        self.menu.addAction(self.stop_focus_action)
        self.menu.addAction(self.open_web_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)

        self.setContextMenu(self.menu)
        self.activated.connect(self.on_activated)
        self.show()

        # 回调函数
        self.show_callback = None
        self.hide_callback = None
        self.exit_callback = None
        self.city_changed_callback = None
        self.focus_mode_callback = None

    def on_show_pets(self):
        if self.show_callback:
            self.show_callback()

    def on_hide_pets(self):
        if self.hide_callback:
            self.hide_callback()

    def on_exit(self):
        if self.exit_callback:
            self.exit_callback()

    def on_set_city(self):
        text, ok = QInputDialog.getText(None, "设置城市", "城市名(拼音或英文):")
        if ok and text.strip():
            if self.city_changed_callback:
                self.city_changed_callback(text.strip())

    def on_start_focus(self):
        minutes, ok = QInputDialog.getInt(None, "专注时长", "请输入专注时长(分钟):", 25, 1, 240)
        if ok:
            self.focus_timer.start_focus(minutes)
            # 通知宠物进入专注模式
            if self.focus_mode_callback:
                self.focus_mode_callback(True)

    def on_stop_focus(self):
        self.focus_timer.stop_focus()
        if self.focus_mode_callback:
            self.focus_mode_callback(False)

    def on_focus_finished(self):
        # 可弹窗或发送通知
        # 这里简单地恢复宠物模式
        if self.focus_mode_callback:
            self.focus_mode_callback(False)

    def on_open_web_climb(self):
        if not self.web_climb_window:
            self.web_climb_window = WebClimbSim(target_window_name="New Tab - Google Chrome")
        self.web_climb_window.show()

    def on_activated(self, reason):
        # 可实现单击打开/关闭宠物等
        pass
