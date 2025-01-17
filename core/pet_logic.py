# core/pet_logic.py

import time
import random
import datetime
from config.states import (
    PetState, TimeState, WeatherType, FestivalType, RandomActionType
)
from config.settings import (
    RANDOM_ACTION_MIN_INTERVAL,
    RANDOM_ACTION_MAX_INTERVAL
)
import math

class PetLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 初始位置
        self.x = screen_width // 2
        self.y = screen_height // 2
        # 速度方向
        self.vx = random.choice([2, -2])
        self.vy = random.choice([2, -2])

        self.current_state = PetState.IDLE
        self.time_state = TimeState.DAY
        self.weather_type = WeatherType.CLEAR
        self.festival_type = FestivalType.NONE

        # 随机动作
        self.last_action_time = time.time()
        self.next_action_time = self._get_next_action_time()

        self.is_in_focus_mode = False  # 专注模式

    def update(self):
        """
        每帧调用：移动、碰撞、随机动作触发
        """
        if self.current_state not in [PetState.DRAGGED, PetState.SLEEPING, PetState.WORKING]:
            self._move()
            self._check_collision()

        # 判断是否可以触发随机动作
        now = time.time()
        if (not self.is_in_focus_mode) and self.current_state == PetState.IDLE and now >= self.next_action_time:
            self.current_state = PetState.RANDOM_ACTION
            action_type = random.choice(list(RandomActionType))
            return action_type
        return None

    def finish_random_action(self):
        self.current_state = PetState.IDLE
        self.last_action_time = time.time()
        self.next_action_time = self._get_next_action_time()

    def set_state(self, new_state):
        self.current_state = new_state

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def _move(self):
        self.x += self.vx
        self.y += self.vy

    def _check_collision(self):
        if self.x <= 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x >= self.screen_width:
            self.x = self.screen_width
            self.vx = -abs(self.vx)

        if self.y <= 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y >= self.screen_height:
            self.y = self.screen_height
            self.vy = -abs(self.vy)

    def update_time_state(self):
        hour = datetime.datetime.now().hour
        if 6 <= hour < 18:
            self.time_state = TimeState.DAY
        else:
            self.time_state = TimeState.NIGHT

    def update_weather(self, weather_type):
        self.weather_type = weather_type

    def update_festival(self, festival_type):
        self.festival_type = festival_type

    def _get_next_action_time(self):
        interval = random.uniform(RANDOM_ACTION_MIN_INTERVAL, RANDOM_ACTION_MAX_INTERVAL)
        return time.time() + interval
