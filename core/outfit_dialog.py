# core/outfit_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from config.settings import ASSETS_DIR
import os

class OutfitDialog(QDialog):
    def __init__(self, pet_logic, unlock_manager, pet_window):
        super().__init__()
        self.pet_logic = pet_logic
        self.unlock_manager = unlock_manager
        self.pet_window = pet_window
        self.setWindowTitle("服装管理")

        layout = QVBoxLayout()
        # 显示全部服装
        all_outfits = list(unlock_manager.outfits.keys())
        for outfit in all_outfits:
            cost = unlock_manager.outfits[outfit]
            btn = QPushButton()

            if outfit in unlock_manager.unlocked_outfits:
                # 已解锁 => “穿上”按钮
                btn.setText(f"{outfit} (已解锁,点击穿上)")
                btn.clicked.connect(lambda _,o=outfit:self.on_wear_outfit(o))
            else:
                # 未解锁 => 显示花费
                btn.setText(f"{outfit} (cost={cost},点击解锁)")
                btn.clicked.connect(lambda _,o=outfit:self.on_unlock_outfit(o))
            layout.addWidget(btn)

        self.setLayout(layout)

    def on_unlock_outfit(self, outfit):
        suc,msg = self.unlock_manager.unlock_outfit(outfit, self.pet_logic)
        if suc:
            print("解锁成功!")
        else:
            print(msg)
        self.close()

    def on_wear_outfit(self, outfit):
        # 让pet_window.current_outfit = bear_outfit_{outfit}.png
        self.pet_window.current_outfit = f"bear_outfit_{outfit}.png"
        print(f"穿上{outfit}")
        self.close()
