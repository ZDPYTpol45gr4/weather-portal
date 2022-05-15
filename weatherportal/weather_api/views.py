import os
import datetime

from django.http import HttpResponseServerError
from django.shortcuts import render

import requests
from .weather_data_class import WeatherInfo

API_KEY = os.getenv('API_KEY')


def get_location(location):
    response_location_coords = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={API_KEY}'
    )

    if not response_location_coords.ok:
        raise ValueError('get_location api response return invalid value')

    get_data_coords = response_location_coords.json()

    if not get_data_coords:  # check if data are available from api
        raise ValueError('Empty data from getting location by location')

    return get_data_coords[0]


def get_all_data_forecast_weather_by_location(location):
    """
    Get weather data from api:
        Current weather
        Minute forecast for 1 hour
        Hourly forecast for 48 hours
        Daily forecast for 7 days
        National weather alerts
        Historical weather data for the previous 5 days
    """

    data_coords = get_location(location)

    lat = data_coords['lat']
    lon = data_coords['lon']

    response_weather = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
    )

    if not response_weather.ok:
        raise ValueError('get_all_data_forecast_weather_by_location api response return invalid value')

    return response_weather.json()


def get_weather(location):
    data = get_all_data_forecast_weather_by_location(location)
    return WeatherInfo.get_weather_list_from_dict(data, get_days_format())


def get_actual_date():
    return datetime.datetime.now()


def get_days_format(days=8):
    """
        Function return list of named days, they are up to param 'days'
    """

    dates = [(get_actual_date() + datetime.timedelta(days=day)).strftime("%A")
             for day in range(days)]
    return dates


def weather_multi_days_view(request, location, day):
    """
        View showing forecast for specific location

        :param location: location, in which weather will be show
        :param day: number of days for forecast
        :return: weather view
    """

    try:
        data = get_weather(location)
    except Exception as e:
        return HttpResponseServerError(f'<h1>{e}</h1>', content_type='text/html')

    if not data:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')

    data = data.weather_data[:day]

    ctx = {'data': data, 'location': location, 'actual_date': get_actual_date()}
    return render(request, 'weather_api/current_weather.html', ctx)
