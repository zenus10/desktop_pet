# core/weather_service.py

import requests
from config.settings import WEATHER_API_KEY, DEFAULT_CITY_NAME
from config.states import WeatherType

class WeatherService:
    def __init__(self, city_name=DEFAULT_CITY_NAME):
        self.city_name = city_name

    def get_weather_type(self):
        """
        返回 WeatherType 枚举，用于桌宠形象/动作的切换
        """
        if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
            # 如果没设置API_KEY，则默认返回CLEAR
            return WeatherType.CLEAR

        url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={WEATHER_API_KEY}"
        try:
            resp = requests.get(url, timeout=5)
            data = resp.json()
            if "weather" in data and len(data["weather"]) > 0:
                main = data["weather"][0]["main"].lower()
                if "rain" in main:
                    return WeatherType.RAIN
                elif "snow" in main:
                    return WeatherType.SNOW
                elif "cloud" in main:
                    return WeatherType.CLOUDY
                else:
                    return WeatherType.CLEAR
            else:
                return WeatherType.CLEAR
        except Exception as e:
            print("WeatherService Error:", e)
            return WeatherType.CLEAR
