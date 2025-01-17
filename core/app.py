# core/app.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from core.multi_pet_manager import MultiPetManager
from core.tray_icon import PetTrayIcon
from core.weather_service import WeatherService
from core.festival_manager import FestivalManager

class PetApp:
    def __init__(self):
        self.pet_manager = MultiPetManager()
        self.tray_icon = PetTrayIcon()

        # 回调绑定
        self.tray_icon.show_callback = self.show_all_pets
        self.tray_icon.hide_callback = self.hide_all_pets
        self.tray_icon.exit_callback = self.exit_app
        self.tray_icon.city_changed_callback = self.on_city_changed
        self.tray_icon.focus_mode_callback = self.on_focus_mode

        # 默认城市
        self.weather_service = WeatherService()
        # 定时更新天气 & 节日
        self.timer_update_external = QTimer()
        self.timer_update_external.timeout.connect(self.update_external_factors)
        self.timer_update_external.start(60_000)  # 1分钟更新一次
        self.update_external_factors()

    def initialize_pets(self, num=1):
        for _ in range(num):
            w = self.pet_manager.create_pet()
            w.show()

    def show_all_pets(self):
        self.pet_manager.show_all()

    def hide_all_pets(self):
        self.pet_manager.hide_all()

    def exit_app(self):
        self.pet_manager.hide_all()
        self.tray_icon.hide()
        QApplication.quit()

    def on_city_changed(self, city_name):
        self.weather_service.city_name = city_name
        self.update_external_factors()

    def on_focus_mode(self, in_focus):
        self.pet_manager.set_focus_mode_for_all(in_focus)

    def update_external_factors(self):
        # 获取天气
        w_type = self.weather_service.get_weather_type()
        self.pet_manager.update_weather_for_all(w_type)

        # 检查节日
        f_type = FestivalManager.check_festival()
        self.pet_manager.update_festival_for_all(f_type)
