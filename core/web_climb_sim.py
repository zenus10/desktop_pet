# core/web_climb_sim.py

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect, QTimer
import win32gui  # 如果在Windows，需要pywin32
import win32ui
import win32con

class WebClimbSim(QWidget):
    """
    简易模拟：截取某个窗口（如Chrome）区域，并在本窗口内显示截图。
    然后把宠物也绘制在此窗口上，营造宠物在网页中爬行的假象。
    """
    def __init__(self, parent=None, target_window_name="Chrome"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)

        self.target_window_name = target_window_name
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_screenshot)
        self.timer.start(1000)  # 每秒刷新截图

        self.resize(800, 600)
        self.show()

    def update_screenshot(self):
        # 查找目标窗口
        hwnd = win32gui.FindWindow(None, self.target_window_name)
        if hwnd:
            # 获取窗口矩形
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top

            hwindc = win32gui.GetWindowDC(hwnd)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()

            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, width, height)
            memdc.SelectObject(bmp)
            memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

            screenshot = bmp.GetBitmapBits(True)
            # 转为 QPixmap
            from PIL import Image
            import io
            im = Image.frombuffer("RGB", (width, height), screenshot, "raw", "BGRX", 0, 1)
            data = io.BytesIO()
            im.save(data, format='BMP')
            qpix = QPixmap()
            qpix.loadFromData(data.getvalue(), 'BMP')

            # 缩放到label大小
            qpix = qpix.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(qpix)

            # 释放
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
