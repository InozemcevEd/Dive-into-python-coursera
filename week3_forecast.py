import sys
import pprint
import requests
from dateutil.parser import parse

# WEATHER FORECAST WITH https://www.weatherapi.com

KEY = "YOUR_KEY"


class WeatherApi:

    def get(self, city):
        url = f"http://api.weatherapi.com/v1/current.json?key={KEY}&q={city}"
        data = requests.get(url).json()
        forecast = [data["current"]["last_updated"], data["current"]["temp_c"]]
        forecast_data = data["current"]
        return forecast


class CityInfo:

    def __init__(self, city, forecast_provider=None):
        self.city = city.lower()
        self._forecast_provider = forecast_provider or WeatherApi()

    def weather_forecast(self):
        return self._forecast_provider.get(self.city)


def _main():
    city_info = sys.argv[1]
    city = CityInfo(city_info)
    forecast = city.weather_forecast()
    pprint.pprint(forecast)


if __name__ == "__main__":
    _main()
