# core/resources_manager.py

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
        path = os.path.join(ASSETS_DIR, "images", filename)
        pixmap = QPixmap(path)
        self.image_cache[filename] = pixmap
        return pixmap

    def load_animation(self, filename):
        if filename in self.animation_cache:
            return self.animation_cache[filename]
        path = os.path.join(ASSETS_DIR, "animations", filename)
        movie = QMovie(path)
        self.animation_cache[filename] = movie
        return movie
