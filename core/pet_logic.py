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
        """
        在pet_window.py的 on_update() 中会调用本函数，
        用来更新宠物的数值和状态（掉落、跑动、随机动作等）。
        """
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        # 1. 在线时长 & 好感度
        self.total_online_secs += dt
        self._check_online_affection()

        # 2. 饥饿度 / 心情
        self.hunger += dt * 0.02
        if self.hunger > 100:
            self.hunger = 100
        self.mood_value -= dt * 0.01
        if self.mood_value < 0:
            self.mood_value = 0

        # 3. 工作/休闲累加
        if self.is_working:
            self.work_time += dt
        else:
            self.rest_time += dt

        # 4. 优先处理FALLING / EDGE_CLING / DRAGGED / WORKING
        if self.current_state == PetState.FALLING:
            self._do_fall(dt)
            return None

        elif self.current_state == PetState.BOUNCE:
            self._do_bounce(dt)
            return None

        elif self.current_state == PetState.EDGE_CLING:
            # 不动（贴在某个边缘）
            return None

        elif self.current_state == PetState.DRAGGED:
            # 由鼠标控制，不自动移动
            return None

        elif self.current_state == PetState.WORKING:
            # 工作状态，不跑不动
            return None

        # 5. 如果是RUN => 继续跑动
        if self.current_state == PetState.RUN:
            self._do_run(dt)

        # 6. 如果IDLE并且到了触发随机的时间 => 跑 or RANDOM_ACTION
        if self.current_state == PetState.IDLE:
            if now >= self.next_action_time:
                # 随机决定跑动 or 进入随机动作
                if random.random() < 0.5:
                    self._start_run()
                else:
                    self.current_state = PetState.RANDOM_ACTION
                    return random.choice(list(RandomActionType))

        # 7. 更新心情枚举
        self._update_mood_state()
        return None

    def _update_mood_state(self):
        if self.mood_value < 20:
            self.mood_state = MoodState.ANGRY
        elif self.mood_value > 80:
            self.mood_state = MoodState.LAUGH
        else:
            self.mood_state = MoodState.NORMAL
        # 可自行再加：if self.mood_value < 10 => CRY

    def finish_random_action(self):
        """
        在pet_window.py里，随机动作播放完后调用。
        """
        self.current_state = PetState.IDLE
        self.next_action_time = self._get_next_action_time()

    def set_state(self, new_state):
        """
        在pet_window里鼠标拖拽/松开、或别的地方都可以用此方法
        """
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
        if self.hunger < 0:
            self.hunger = 0
        self.mood_value += mood_boost
        if self.mood_value > 100:
            self.mood_value = 100

    def click_interaction(self, mood_boost=3):
        self.mood_value += mood_boost
        if self.mood_value > 100:
            self.mood_value = 100

    def _check_online_affection(self):
        """
        每10分钟(600秒)加10好感度
        """
        cur_milestones = int(self.total_online_secs // 600)
        if cur_milestones > self.online_milestones:
            newly = cur_milestones - self.online_milestones
            self.affection += newly * 10
            self.online_milestones = cur_milestones

    def _start_run(self):
        """
        切换到RUN状态，并设置随机vx,vy,跑一段时间后回IDLE
        """
        self.current_state = PetState.RUN
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.run_start_time = time.time()
        self.run_duration = random.uniform(1.5, 3.0)
        # 在跑完后才触发下一次动作
        self.next_action_time = time.time() + self.run_duration

    def _do_run(self, dt):
        """
        跑动逻辑：每帧移动(x,y)，若碰到屏幕边缘则反弹。
        过了run_duration，就回到IDLE
        """
        self.x += self.vx
        self.y += self.vy
        # 边界反弹
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x > self.screen_width:
            self.x = self.screen_width
            self.vx = -abs(self.vx)

        if self.y < 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y > self.screen_height:
            self.y = self.screen_height
            self.vy = -abs(self.vy)

        if time.time() - self.run_start_time >= self.run_duration:
            # 跑完 => 回到IDLE
            self.current_state = PetState.IDLE

    def _get_next_action_time(self):
        return time.time() + random.uniform(RANDOM_ACTION_MIN_INTERVAL, RANDOM_ACTION_MAX_INTERVAL)

    # ---------------- FALLING/EDGE_CLING 逻辑整合 ----------------
    def _do_fall(self, dt):
        """
        简易掉落逻辑： 模拟重力加速度
        """
        gravity = 9.8
        
        # vx可保留也可置0
        self.vy += gravity * dt
        self.y += self.vy
        # 若到底
        if self.y >= self.screen_height:
            # 到达地面
            self.y = self.screen_height
            # 可以让反弹速度基于当前下落速度衰减，也可用固定值
            # 例：衰减50%
            #  vy = -abs(self.vy) * 0.5
            # 例：固定速度 -200
            self.vy = -abs(self.vy) * 0.5

            # 切换到 BOUNCE 状态 (向上弹)
            self.current_state = PetState.BOUNCE

    def _do_bounce(self, dt):
        """
        BOUNCE: 从地面往上抛, gravity依然为正(地球向下),
        vy开始是负的(向上). 当 vy>=0 => 到最高点, 立即静止(IDLE).
        """
        gravity = 9.8
        # 速度加重力(向下)
        self.vy += gravity * dt
        self.y += self.vy

        # 如果 y<0 可以限制, 也可不理
        if self.y < 0:
            self.y = 0
            self.vy = 0
            self.current_state = PetState.IDLE
            return

        # 当上抛到 vy >= 0 => 说明速度变正(最高点或往下)
        if self.vy >= 0:
            # 不再往下落 => 只弹一次就停
            self.vy = 0
            self.current_state = PetState.IDLE
