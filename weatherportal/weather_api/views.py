import os

from django.shortcuts import render
import requests

API_KEY = os.getenv('API_KEY')


def get_location(location):
    response_location_coords = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={API_KEY}'
        )

    get_data_coords = response_location_coords.json()
    return get_data_coords[0]


def get_all_data_forecast_weather_by_location(request):
    """
    Get weather data from api:
        Current weather
        Minute forecast for 1 hour
        Hourly forecast for 48 hours
        Daily forecast for 7 days
        National weather alerts
        Historical weather data for the previous 5 days
    """

    data_coords = get_location("London")

    lat = data_coords['lat']
    lon = data_coords['lon']

    response_weather = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
        )
    get_data_weather = response_weather.json()

    return get_data_weather


def get_current_weather_by_location(location):
    """
    Get current weather from specific location
    """
    data_coords = get_location(location)

    lat = data_coords['lat']
    lon = data_coords['lon']

    response_weather = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
        )
    get_data_weather = response_weather.json()

    return get_data_weather


def weather_7_days_view(request):
    data = get_all_data_forecast_weather_by_location('London')
    temperature = [val['temp'] for val in data['daily']]
    day1 = temperature[1]
    day2 = temperature[2]
    day3 = temperature[3]
    day4 = temperature[4]
    day5 = temperature[5]
    day6 = temperature[6]
    day7 = temperature[7]
    ctx = {'temperature': temperature, 'day1': day1, 'day2': day2,
           'day3': day3, 'day4': day4, 'day5': day5, 'day6': day6,
           'day7': day7
           }
    return render(request, 'weather_api/current_weather.html', ctx)