# core/focus_timer.py

from PyQt5.QtCore import QTimer, pyqtSignal, QObject

class FocusTimer(QObject):
    """
    简易番茄钟：设置一个倒计时（分钟），触发完成信号。
    """
    focus_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.remaining_seconds = 0

    def start_focus(self, minutes=25):
        self.remaining_seconds = minutes * 60
        self.timer.start(1000)  # 每秒tick

    def stop_focus(self):
        self.timer.stop()
        self.remaining_seconds = 0

    def _tick(self):
        self.remaining_seconds -= 1
        if self.remaining_seconds <= 0:
            self.timer.stop()
            # 触发完成信号
            self.focus_finished.emit()
