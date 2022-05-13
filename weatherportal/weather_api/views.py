import os
import datetime

from django.http import HttpResponseServerError
from django.shortcuts import render, redirect

import requests
from .weather_data_class import WeatherInfo

API_KEY = os.getenv('API_KEY')


def get_location(location):
    try:
        response_location_coords = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={API_KEY}'
        )
        get_data_coords = response_location_coords.json()

        return get_data_coords[0]

    except IndexError:
        return None


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
    if data_coords:  # check if data are avaliable from api

        lat = data_coords['lat']
        lon = data_coords['lon']
        try:
            response_weather = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
            )
            get_data_weather = response_weather.json()

            return WeatherInfo.get_dict_for_daily(get_data_weather, get_days_format())
        except requests.exceptions.HTTPError:
            return None
    else:
        return None


def get_actual_date():
    return datetime.datetime.now()


def get_days_format(days=8):
    """
    Function return list of named days, they are up to param 'days'
    """
    dates = [(get_actual_date() + datetime.timedelta(days=day)).strftime("%A")
             for day in range(days)]
    return dates


def weather_7_days_view(request, location):
    data = get_all_data_forecast_weather_by_location(location)
    if not data:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')


    ctx = {'data': data.data, 'location': location, 'actual_date': get_actual_date()}
    return render(request, 'weather_api/current_weather.html', ctx)
