# core/pet_window.py

from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QPixmap, QMovie
from config.states import (
    PetState, TimeState, WeatherType, FestivalType, RandomActionType
)
from config.settings import (
    DEFAULT_WIDTH, DEFAULT_HEIGHT, UPDATE_INTERVAL_MS
)
from core.resources_manager import ResourcesManager
from core.file_drag_sim import FileDragSim

class PetWindow(QWidget):
    def __init__(self, pet_logic):
        super().__init__()
        self.pet_logic = pet_logic
        self.res_manager = ResourcesManager()

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT)

        self.file_drag_sim = FileDragSim(parent=self)

        self._init_window()
        self._init_timer()

        self.is_dragging = False
        self.drag_position = QPoint()

        self.current_action = None
        self.movie = None

        # 初始化形象
        self._update_appearance()

    def _init_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.move(self.pet_logic.x, self.pet_logic.y)

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_update)
        self.timer.start(UPDATE_INTERVAL_MS)

    def on_update(self):
        # 更新外部因素
        self.pet_logic.update_time_state()

        # 更新逻辑
        action_type = self.pet_logic.update()
        if action_type is not None:
            self._play_random_action(action_type)

        # 同步位置
        self.move(self.pet_logic.x, self.pet_logic.y)

        # 若处于随机动作状态，判断是否结束
        self._maybe_finish_action()

        # 根据日夜、天气、节日等更新静态形象(若当前是IDLE)
        if self.pet_logic.current_state == PetState.IDLE:
            self._update_appearance()

    def _play_random_action(self, action_type):
        self.current_action = action_type
        # 随机动作对应不同 GIF
        if action_type == RandomActionType.DRINK:
            self._set_gif("bear_drink.gif")
        elif action_type == RandomActionType.EAT:
            self._set_gif("bear_eat.gif")
        elif action_type == RandomActionType.DANCE:
            self._set_gif("bear_dance.gif")
        elif action_type == RandomActionType.FACEMASK:
            self._set_gif("bear_facemask.gif")
        elif action_type == RandomActionType.WATCH_PHONE:
            self._set_gif("bear_watch_phone.gif")
        else:
            self._set_image("bear_idle_day.png")

    def _maybe_finish_action(self):
        """
        简易处理：随机动作播放约3秒后结束，回到IDLE
        可用更多精细逻辑：检测GIF播放次数等
        """
        # 这里可以加一个时间戳判断
        # 为了简化，每次播放后在这里直接写死时长
        pass

    def finish_current_action(self):
        self.current_action = None
        self.pet_logic.finish_random_action()
        self._update_appearance()

    def _update_appearance(self):
        """
        根据day/night, weather, festival 选择不同图片
        """
        if self.pet_logic.festival_type == FestivalType.CHRISTMAS:
            self._set_image("bear_festival_christmas.png")
            return
        elif self.pet_logic.festival_type == FestivalType.HALLOWEEN:
            self._set_image("bear_festival_halloween.png")
            return

        # 若节日不匹配，则看天气
        if self.pet_logic.weather_type == WeatherType.RAIN:
            self._set_image("bear_rain.png")
        elif self.pet_logic.weather_type == WeatherType.SNOW:
            self._set_image("bear_snow.png")
        else:
            # 若无雨无雪，则分日夜
            if self.pet_logic.time_state == TimeState.DAY:
                self._set_image("bear_idle_day.png")
            else:
                self._set_image("bear_idle_night.png")

    def _set_image(self, filename):
        if self.movie:
            self.movie.stop()
            self.movie = None
        pixmap = self.res_manager.load_image(filename)
        if pixmap.isNull():
            return
        scaled = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)

    def _set_gif(self, filename):
        if self.movie:
            self.movie.stop()
        self.movie = self.res_manager.load_animation(filename)
        self.label.setMovie(self.movie)
        self.movie.start()

    # ============ 拖拽相关 ============
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.pet_logic.set_state(PetState.DRAGGED)

            # 模拟抓文件
            self.file_drag_sim.show_near_pet(self.pet_logic.x, self.pet_logic.y)

            # 如果在做随机动作，结束
            if self.current_action:
                self.finish_current_action()

            event.accept()

    def mouseMoveEvent(self, event):
        if self.is_dragging and (event.buttons() & Qt.LeftButton):
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            self.pet_logic.set_position(new_pos.x(), new_pos.y())
            # 同步文件拖拽位置
            self.file_drag_sim.show_near_pet(new_pos.x(), new_pos.y())
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.pet_logic.set_state(PetState.IDLE)
            # 重置文件图标
            self.file_drag_sim.reset_icon()
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.end()
