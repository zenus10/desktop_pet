# core/multi_pet_manager.py

from PyQt5.QtGui import QGuiApplication
from core.pet_logic import PetLogic
from core.pet_window import PetWindow

class MultiPetManager:
    def __init__(self):
        self.pet_windows = []
        screen_rect = QGuiApplication.primaryScreen().availableGeometry()
        self.screen_width = screen_rect.width() - 50
        self.screen_height = screen_rect.height() - 50

    def create_pet(self):
        logic = PetLogic(self.screen_width, self.screen_height)
        window = PetWindow(logic)
        self.pet_windows.append((logic, window))
        return window

    def show_all(self):
        for logic, w in self.pet_windows:
            w.show()

    def hide_all(self):
        for logic, w in self.pet_windows:
            w.hide()

    def update_weather_for_all(self, weather_type):
        for logic, w in self.pet_windows:
            logic.update_weather(weather_type)

    def update_festival_for_all(self, festival_type):
        for logic, w in self.pet_windows:
            logic.update_festival(festival_type)

    def set_focus_mode_for_all(self, in_focus):
        """
        若in_focus=True，则让宠物进入WORKING或SLEEPING状态
        """
        for logic, w in self.pet_windows:
            logic.is_in_focus_mode = in_focus
            if in_focus:
                logic.set_state(PetState.WORKING)  # or SLEEPING
            else:
                logic.set_state(PetState.IDLE)
