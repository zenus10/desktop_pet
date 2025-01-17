# config/settings.py

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# 默认窗口大小
DEFAULT_WIDTH = 200
DEFAULT_HEIGHT = 200

# 刷新间隔（毫秒）——影响动画、逻辑刷新
UPDATE_INTERVAL_MS = 30

# 随机动作触发时间区间（秒）
RANDOM_ACTION_MIN_INTERVAL = 10
RANDOM_ACTION_MAX_INTERVAL = 20

# 托盘图标路径
TRAY_ICON_PATH = os.path.join(ASSETS_DIR, "animations", "bear_idle_day.png")

# 天气API配置（以OpenWeatherMap示例，需要自行注册获取API_KEY）
WEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
DEFAULT_CITY_NAME = "Beijing"

# 一些节日的日期（仅示例）
FESTIVALS = {
    "CHRISTMAS": (12, 25),
    "HALLOWEEN": (10, 31),
    # 可扩展更多，如春节(农历)，此处暂不实现农历推算
}

# 专注时长默认值（分钟）
DEFAULT_FOCUS_MINUTES = 25
