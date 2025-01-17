import time
import random
from config.states import PetState, MoodState, RandomActionType
from config.settings import (
    RANDOM_ACTION_MIN_INTERVAL, RANDOM_ACTION_MAX_INTERVAL
)

class PetLogic:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2

        self.current_state = PetState.IDLE
        self.mood_state = MoodState.NORMAL

        self.total_online_secs = 0
        self.online_milestones = 0
        self.affection = 0

        self.hunger = 0    # 0~100
        self.mood_value = 50  # 0~100

        self.is_working = False
        self.work_time = 0
        self.rest_time = 0
        self.last_mode_change = time.time()

        self.last_update_time = time.time()
        self.next_action_time = self._get_next_action_time()

        # 跑动的一些临时参数
        self.vx = 0
        self.vy = 0
        self.run_start_time = 0
        self.run_duration = 2  # 跑2秒

    def update(self):
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        # 在线时长
        self.total_online_secs += dt
        self._check_online_affection()

        # 饥饿度 & 心情值简单随时间变化
        self.hunger += dt*0.02
        if self.hunger>100: self.hunger=100
        self.mood_value -= dt*0.01
        if self.mood_value<0: self.mood_value=0

        # 工作/休闲累加
        if self.is_working:
            self.work_time += dt
        else:
            self.rest_time += dt

        # 如果 RUN => 移动
        if self.current_state == PetState.RUN:
            self._do_run(dt)

        # 如果 idle 并到时间 => 决定是“跑一下” 还是 “随机动作”
        if self.current_state == PetState.IDLE:
            if now >= self.next_action_time:
                do_run = random.choice([True, False])  # 50%几率跑一下
                if do_run:
                    self._start_run()
                else:
                    # RANDOM_ACTION
                    self.current_state = PetState.RANDOM_ACTION
                    return random.choice(list(RandomActionType))

        self._update_mood_state()
        return None

    def _update_mood_state(self):
        if self.mood_value < 20:
            self.mood_state = MoodState.ANGRY
        elif self.mood_value > 80:
            self.mood_state = MoodState.LAUGH
        else:
            self.mood_state = MoodState.NORMAL
        # 也可加分支 if <10 => cry

    def finish_random_action(self):
        self.current_state = PetState.IDLE
        self.next_action_time = self._get_next_action_time()

    def set_state(self, new_state):
        self.current_state = new_state

    def set_work_mode(self, working):
        self.is_working = working
        if working:
            self.current_state = PetState.WORKING
        else:
            self.current_state = PetState.IDLE
        self.last_mode_change = time.time()

    def feed(self, food_value, mood_boost):
        self.hunger -= food_value
        if self.hunger<0: self.hunger=0
        self.mood_value += mood_boost
        if self.mood_value>100: self.mood_value=100

    def click_interaction(self, mood_boost=3):
        self.mood_value += mood_boost
        if self.mood_value>100: self.mood_value=100

    def _check_online_affection(self):
        cur_milestones = int(self.total_online_secs//600)
        if cur_milestones> self.online_milestones:
            newly = cur_milestones - self.online_milestones
            self.affection += newly*10
            self.online_milestones = cur_milestones

    def _start_run(self):
        self.current_state = PetState.RUN
        # 赋随机速度
        self.vx = random.uniform(-3,3)
        self.vy = random.uniform(-3,3)
        self.run_start_time = time.time()
        self.run_duration = random.uniform(1.5,3.0)
        # 预设next_action_time在跑完后才产生新的随机动作
        self.next_action_time = time.time()+self.run_duration

    def _do_run(self, dt):
        self.x += self.vx
        self.y += self.vy
        # 碰撞
        if self.x<0:
            self.x=0
            self.vx = abs(self.vx)
        elif self.x>self.screen_width:
            self.x=self.screen_width
            self.vx = -abs(self.vx)
        if self.y<0:
            self.y=0
            self.vy = abs(self.vy)
        elif self.y>self.screen_height:
            self.y=self.screen_height
            self.vy = -abs(self.vy)

        if time.time() - self.run_start_time >= self.run_duration:
            # 跑完了 => idle
            self.current_state = PetState.IDLE

    def _get_next_action_time(self):
        return time.time() + random.uniform(RANDOM_ACTION_MIN_INTERVAL, RANDOM_ACTION_MAX_INTERVAL)
    
    def update(self):
        # ...
        if self.current_state == PetState.FALLING:
            self._do_fall(dt)
        elif self.current_state == PetState.EDGE_CLING:
            # 处于趴在边缘状态 => 不移动，或者贴边
            pass
        # ...

    def _do_fall(self, dt):
        # 简易: y往下加速
        gravity = 9.8
        self.vy += gravity * dt
        self.y += self.vy
        # 如果y>屏幕底 => idle
        if self.y>=self.screen_height:
            self.y = self.screen_height
            self.vy = 0
            self.set_state(PetState.IDLE)
            # 也可播“摔倒”动画
