from geopy.geocoders import Nominatim
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()


def write_env(name, data):
    with open(".env", "a") as f:
        f.write(f"{name.upper()}={data}\n")
        f.close()


def detect_exists_env(check_name):
    with open(".env", "r") as f:
        for data in f.readlines():
            name = data.split('=')
            if name[0] == check_name.upper():
                return True, name[1]
    return False, None


def detect_location_data():
    if os.path.isfile('location_data.json'):
        return True
    else:
        return False


class Weather:
    def __init__(self, location=None) -> None:
        self.weather_status = None
        self.api = os.getenv('WEATHER_API')

        self.address, self.lat, self.lon = self.get_weather(location)

    @ staticmethod
    def get_weather(loc):
        try:
            geolocator = Nominatim(user_agent="stella")
            location = geolocator.geocode(loc)
            return location.address, location.latitude, location.longitude
        except ConnectionError:
            raise 'no connection'

    def get_json(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.api}"
        res = requests.get(url)
        data = json.loads(res.text)
        return data

    def new(self, sentence=True):
        json_data = self.get_json()
        weather = json_data['weather'][0]
        status = weather['main']
        name = json_data['name']
        description = weather['description']
        icon = weather['icon']
        temp = json_data["main"]['temp'] - 273.15
        humidity = json_data["main"]['humidity']
        temp_max = json_data["main"]['temp_max'] - 273.15
        temp_min = json_data["main"]['temp_min'] - 273.15
        feel = json_data["main"]["feels_like"] - 273.15
        pressure = json_data['main']['pressure']
        wind_speed = json_data['wind']['speed'] * 2.23694
        wind_deg = json_data['wind']['deg']
        wind_types = self.wind_type(wind_speed)
        if sentence:
            return f'The weather in {name} is currently {round(temp,1)} degrees with {description} and the wind is {wind_types}.'
        else:
            return name, round(temp, 1), description, wind_types, round(wind_speed, 1), pressure, humidity, round(temp_max, 1), round(temp_min, 1), icon, round(feel, 1), status, wind_deg, self.address

    @ staticmethod
    def wind_type(windspeed):
        windspeed = int(round(windspeed, 1))
        if windspeed < 1:
            return 'clam'
        elif 1 <= windspeed <= 3:
            return 'light air'
        elif 4 <= windspeed <= 7:
            return 'light breeze'
        elif 8 <= windspeed <= 12:
            return 'gentle breeze'
        elif 13 <= windspeed <= 18:
            return 'moderate breeze'
        elif 19 <= windspeed <= 24:
            return 'fresh breeze'
        elif 25 <= windspeed <= 31:
            return 'strong breeze'
        elif 32 <= windspeed <= 38:
            return 'near gale'
        elif 39 <= windspeed <= 46:
            return 'gale'
        elif 47 <= windspeed <= 54:
            return 'strong gale'
        elif 55 <= windspeed <= 63:
            return 'whole gale'
        elif 64 <= windspeed <= 75:
            return 'storm force'
        elif windspeed >= 75:
            return 'hurricane force'
        else:
            return 'error'


if __name__ == "__main__":
    print(Weather().new())
