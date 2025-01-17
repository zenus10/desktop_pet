# config/states.py

from enum import Enum, auto

class PetState(Enum):
    IDLE = auto()
    RANDOM_ACTION = auto()
    DRAGGED = auto()
    SLEEPING = auto()
    WORKING = auto()

class TimeState(Enum):
    DAY = auto()
    NIGHT = auto()

class WeatherType(Enum):
    CLEAR = auto()
    RAIN = auto()
    SNOW = auto()
    CLOUDY = auto()

class RandomActionType(Enum):
    DRINK = auto()
    EAT = auto()
    DANCE = auto()
    FACEMASK = auto()
    WATCH_PHONE = auto()
    # etc.

class FestivalType(Enum):
    NONE = auto()
    CHRISTMAS = auto()
    HALLOWEEN = auto()
    # etc.
