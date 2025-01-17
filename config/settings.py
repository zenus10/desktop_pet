import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 200

UPDATE_INTERVAL_MS = 30  # 刷新间隔(ms)

TRAY_ICON_PATH = os.path.join(ASSETS_DIR, "images", "tray_icon.png")
FILE_ICON_PATH = os.path.join(ASSETS_DIR, "images", "file_icon.png")

# 随机动作区间
RANDOM_ACTION_MIN_INTERVAL = 4
RANDOM_ACTION_MAX_INTERVAL = 7
