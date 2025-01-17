from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QAction, QInputDialog
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QMovie
from config.states import PetState, MoodState, RandomActionType
from config.settings import DEFAULT_WIDTH, DEFAULT_HEIGHT, UPDATE_INTERVAL_MS
from core.resources_manager import ResourcesManager
from core.file_drag_sim import FileDragSim

class PetWindow(QWidget):
    def __init__(self, pet_logic, unlock_manager):
        super().__init__()
        self.pet_logic = pet_logic
        self.unlock_manager = unlock_manager
        self.res_manager = ResourcesManager()

        self.scale_factor = 1.0
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setGeometry(0, 0, DEFAULT_WIDTH, DEFAULT_HEIGHT)

        self.file_drag_sim = FileDragSim(self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.resize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.move(self.pet_logic.x, self.pet_logic.y)

        self.timer = QTimer(self)
        self.move(int(self.pet_logic.x), int(self.pet_logic.y))
        self.timer.timeout.connect(self.on_update)
        self.timer.start(UPDATE_INTERVAL_MS)

        self.is_dragging = False
        self.drag_position = QPoint()

        self.movie = None
        self.current_action = None
        self.current_outfit = None  # 当前穿的服装(静态PNG)

    def on_update(self):
        res = self.pet_logic.update()
        if res:
            self._play_random_action(res)

        self.move(self.pet_logic.x, self.pet_logic.y)

        # 根据pet_logic的state决定显示
        st = self.pet_logic.current_state
        if st == PetState.IDLE:
            self._update_idle_appearance()
        elif st == PetState.RUN:
            self._set_gif("bear_run.gif")
        elif st == PetState.WORKING:
            # 显示一个"工作"动画(可换别的)
            self._set_gif("bear_work.gif")
        # else: DRAGGED在mousePress
        # RANDOM_ACTION => 播放完后回Idle
       
        if st == PetState.FALLING:
            self._set_gif("bear_fall.gif")
        elif st == PetState.EDGE_CLING:
            self._set_gif("bear_edge_cling.gif")


    def _update_idle_appearance(self):
        # 看mood_state
        ms = self.pet_logic.mood_state
        if ms == MoodState.ANGRY:
            self._set_gif("bear_angry.gif")
        elif ms == MoodState.CRY:
            self._set_gif("bear_cry.gif")
        elif ms == MoodState.LAUGH:
            self._set_gif("bear_laugh.gif")
        else:
            # 如果有outfit就显示它,否则bear_idle.png
            if self.current_outfit:
                self._set_image(self.current_outfit)
            else:
                self._set_image("bear_idle.png")

    def _play_random_action(self, act_type):
        self.current_action = act_type
        if act_type == RandomActionType.EAT:
            self._set_gif("bear_eat.gif")
        elif act_type == RandomActionType.DRINK:
            self._set_gif("bear_drink.gif")
        elif act_type == RandomActionType.DANCE:
            self._set_gif("bear_dance.gif")

    def finish_current_action(self):
        self.current_action = None
        self.pet_logic.finish_random_action()

    def set_scale(self, scale_factor):
        self.scale_factor = scale_factor
        w = int(DEFAULT_WIDTH*scale_factor)
        h = int(DEFAULT_HEIGHT*scale_factor)
        self.resize(w, h)
        self.label.setGeometry(0, 0, w, h)

    # ============ 交互 ============
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.pet_logic.set_state(PetState.DRAGGED)
            self._set_gif("bear_dragged.gif")
            self.file_drag_sim.show_near_pet(self.pet_logic.x, self.pet_logic.y)
            # 点击增加心情
            self.pet_logic.click_interaction(3)
            # 如果在random_action, 结束之
            if self.current_action:
                self.finish_current_action()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            # 判断是否在边缘
            x_margin = 50
            y_margin = 50
            if self.pet_logic.x < x_margin:
                # 靠左边缘 => 进入EDGE_CLING
                self.pet_logic.set_state(PetState.EDGE_CLING)
                # 也可以在pet_logic中记录是左边缘
            elif (self.pet_logic.screen_width - self.pet_logic.x) < x_margin:
                # 右边缘
                self.pet_logic.set_state(PetState.EDGE_CLING)
            elif (self.pet_logic.screen_height - self.pet_logic.y) < y_margin:
                # 下边缘
                self.pet_logic.set_state(PetState.EDGE_CLING)
            else:
                # 否则掉落
                self.pet_logic.set_state(PetState.FALLING)
            
            self.file_drag_sim.reset_icon()
            event.accept()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.pet_logic.set_state(PetState.IDLE)
            self.file_drag_sim.reset_icon()
            event.accept()

    def show_context_menu(self, global_pos):
        menu = QMenu()

        # 信息:好感/饥饿/在线秒
        info_str = (f"好感:{self.pet_logic.affection}  "
                    f"饥饿:{int(self.pet_logic.hunger)}  "
                    f"心情:{int(self.pet_logic.mood_value)}  "
                    f"在线:{int(self.pet_logic.total_online_secs)}s")
        info_action = QAction(info_str, self)
        info_action.setEnabled(False)
        menu.addAction(info_action)

        # 工作模式
        toggle_work = QAction("切换工作状态", self)
        toggle_work.triggered.connect(self.on_toggle_work)
        menu.addAction(toggle_work)

        outfit_action = QAction("服装管理", self)
        outfit_action.triggered.connect(self.on_outfit_dialog)
        menu.addAction(outfit_action)

        food_action = QAction("食物管理", self)
        food_action.triggered.connect(self.on_food_dialog)
        menu.addAction(food_action)

        toggle_hide_action = QAction("隐藏宠物", self, checkable=True)
        toggle_hide_action.setChecked(False)
        toggle_hide_action.triggered.connect(self.on_toggle_hide)
        menu.addAction(toggle_hide_action)

        menu.exec_(global_pos)

    def on_toggle_hide(self, checked):
        if checked:
            self.hide()
        else:
            self.show()

    def on_outfit_dialog(self):
        from core.outfit_dialog import OutfitDialog
        dlg = OutfitDialog(self.pet_logic, self.unlock_manager, self)
        dlg.exec_()

    def on_food_dialog(self):
        from core.food_dialog import FoodDialog
        dlg = FoodDialog(self.pet_logic, self.unlock_manager, self)
        dlg.exec_()

    def on_toggle_work(self):
        self.pet_logic.set_work_mode(not self.pet_logic.is_working)

    def on_buy_outfit(self):
        outfit_name, ok = QInputDialog.getText(None, "购买服装", "输入服装名:")
        if ok and outfit_name:
            suc, msg = self.unlock_manager.unlock_outfit(outfit_name, self.pet_logic)
            print(msg)

    def on_change_outfit(self):
        outfits = self.unlock_manager.get_unlocked_outfits()
        if not outfits:
            print("暂无已解锁服装")
            return
        choice, ok = QInputDialog.getItem(None, "更换服装", "已解锁:", outfits, 0, False)
        if ok and choice:
            self.current_outfit = f"bear_outfit_{choice}.png"
            print(f"换上{choice}服装")

    def on_buy_food(self):
        food_name, ok = QInputDialog.getText(None, "购买食物", "输入食物名:")
        if ok and food_name:
            suc, msg = self.unlock_manager.unlock_food(food_name, self.pet_logic)
            print(msg)

    def on_feed_pet(self):
        foods = self.unlock_manager.get_unlocked_foods()
        if not foods:
            print("无已解锁食物")
            return
        choice, ok = QInputDialog.getItem(None, "投喂", "已解锁食物:", foods, 0, False)
        if ok and choice:
            # 简易示例: snack => feed(10,5), cake => feed(20,10)
            if choice=="snack":
                self.pet_logic.feed(10,5)
                self._set_gif("bear_eat.gif")
            elif choice=="cake":
                self.pet_logic.feed(20,10)
                self._set_gif("bear_eat.gif")

    # ============ 绘制 ============
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.end()

    def _set_image(self, filename):
        if self.movie:
            self.movie.stop()
            self.movie = None
        pix = self.res_manager.load_image(filename)
        if pix:
            w = int(DEFAULT_WIDTH*self.scale_factor)
            h = int(DEFAULT_HEIGHT*self.scale_factor)
            scaled = pix.scaled(w,h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled)

    def _set_gif(self, filename):
        if self.movie:
            self.movie.stop()
        mv = self.res_manager.load_animation(filename)
        if mv:
            self.movie = mv
            self.label.setMovie(self.movie)
            self.movie.start()
