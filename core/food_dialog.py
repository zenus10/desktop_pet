# core/food_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
class FoodDialog(QDialog):
    def __init__(self, pet_logic, unlock_manager, pet_window):
        super().__init__()
        self.pet_logic = pet_logic
        self.unlock_manager = unlock_manager
        self.pet_window = pet_window
        self.setWindowTitle("食物管理")

        layout = QVBoxLayout()

        all_foods = list(unlock_manager.foods.keys())
        for food in all_foods:
            cost = unlock_manager.foods[food]
            btn = QPushButton()
            if food in unlock_manager.unlocked_foods:
                btn.setText(f"{food} (已解锁, 点击投喂)")
                btn.clicked.connect(lambda _,f=food:self.on_feed(f))
            else:
                btn.setText(f"{food} (cost={cost},点击解锁)")
                btn.clicked.connect(lambda _,f=food:self.on_unlock_food(f))

            layout.addWidget(btn)

        self.setLayout(layout)

    def on_unlock_food(self, food):
        suc,msg = self.unlock_manager.unlock_food(food, self.pet_logic)
        print(msg)
        self.close()

    def on_feed(self, food):
        # 例: snack=> feed(10,5), cake=> feed(20,10)
        if food=="snack":
            self.pet_logic.feed(10,5)
            self.pet_window._set_gif("bear_eat.gif")
        elif food=="cake":
            self.pet_logic.feed(20,10)
            self.pet_window._set_gif("bear_eat.gif")

        self.close()
