# core/festival_manager.py

import datetime
from config.settings import FESTIVALS
from config.states import FestivalType

class FestivalManager:
    @staticmethod
    def check_festival():
        today = datetime.date.today()
        for festival_name, (month, day) in FESTIVALS.items():
            if today.month == month and today.day == day:
                if festival_name.upper() == "CHRISTMAS":
                    return FestivalType.CHRISTMAS
                elif festival_name.upper() == "HALLOWEEN":
                    return FestivalType.HALLOWEEN
        return FestivalType.NONE
