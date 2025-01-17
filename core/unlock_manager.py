class UnlockManager:
    def __init__(self):
        self.outfits = {
            "raincoat": 50,
            "snowcoat": 80
        }
        self.unlocked_outfits = set()

        self.foods = {
            "snack":  20,  # cost
            "cake":   40
        }
        self.unlocked_foods = set()

    def unlock_outfit(self, outfit_name, pet_logic):
        if outfit_name not in self.outfits:
            return False, "服装不存在"
        cost = self.outfits[outfit_name]
        if outfit_name in self.unlocked_outfits:
            return True, "已解锁"
        if pet_logic.affection >= cost:
            pet_logic.affection -= cost
            self.unlocked_outfits.add(outfit_name)
            return True, "解锁成功"
        else:
            return False, "好感度不足"

    def unlock_food(self, food_name, pet_logic):
        if food_name not in self.foods:
            return False, "食物不存在"
        cost = self.foods[food_name]
        if food_name in self.unlocked_foods:
            return True, "已解锁"
        if pet_logic.affection >= cost:
            pet_logic.affection -= cost
            self.unlocked_foods.add(food_name)
            return True, "解锁成功"
        else:
            return False, "好感度不足"

    def get_unlocked_outfits(self):
        return list(self.unlocked_outfits)

    def get_unlocked_foods(self):
        return list(self.unlocked_foods)
