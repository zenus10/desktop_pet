import os
from PyQt5.QtGui import QPixmap, QMovie
from config.settings import ASSETS_DIR

class ResourcesManager:
    def __init__(self):
        self.image_cache = {}
        self.animation_cache = {}

    def load_image(self, filename):
        if filename in self.image_cache:
            return self.image_cache[filename]
        path_img = os.path.join(ASSETS_DIR, "images", filename)
        if os.path.exists(path_img):
            pix = QPixmap(path_img)
            self.image_cache[filename] = pix
            return pix
        path_anim = os.path.join(ASSETS_DIR, "animations", filename)
        if os.path.exists(path_anim):
            pix = QPixmap(path_anim)
            self.image_cache[filename] = pix
            return pix
        print(f"[WARN] load_image failed: {filename}")
        return None

    def load_animation(self, filename):
        if filename in self.animation_cache:
            return self.animation_cache[filename]
        path_img = os.path.join(ASSETS_DIR, "images", filename)
        path_anim = os.path.join(ASSETS_DIR, "animations", filename)
        if os.path.exists(path_img):
            mv = QMovie(path_img)
            self.animation_cache[filename] = mv
            return mv
        elif os.path.exists(path_anim):
            mv = QMovie(path_anim)
            self.animation_cache[filename] = mv
            return mv
        print(f"[WARN] load_animation failed: {filename}")
        return None
