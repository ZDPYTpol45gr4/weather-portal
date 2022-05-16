import datetime
import os

import requests
from django.http import HttpResponseServerError
from django.shortcuts import render

from .data_classes import WeatherInfo
from .exceptions import exception_check, ServerResponseError
from .validators import Validator

API_KEY = os.getenv('API_KEY')


def get_location(location):
    response_location_coords = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={API_KEY}'
    )

    if not response_location_coords.ok:
        raise ServerResponseError(
            'location api response return status_code higher then 400'
        )

    get_data_coords = response_location_coords.json()
    Validator.validate_location(get_data_coords)

    return get_data_coords


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

    data_coords = get_location(location)[0]

    lat = data_coords['lat']
    lon = data_coords['lon']

    response_weather = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={API_KEY}'
    )

    if not response_weather.ok:
        raise ServerResponseError(
            'get_all_data_forecast_weather_by_location api response return status_code higher then 400'
        )

    return response_weather.json()


def get_weather(location):
    """
        Get weather and validate data
    """
    data = get_all_data_forecast_weather_by_location(location)
    Validator.validate_weather(data)

    return WeatherInfo.get_weather_list_from_dict(data, get_days_format())


def get_days_format():
    """
        Function return list of named days, they are up to param 'days'
    """
    DAYS_NUMBER = 8

    dates = [(datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%A")
             for day in range(DAYS_NUMBER)]
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
    except Exception as exce:
        message = exception_check(exce)
        return HttpResponseServerError(message, content_type='text/html')

    data = data.weather_data[:day]

    ctx = {'data': data, 'location': location, 'actual_date': datetime.datetime.now()}
    return render(request, 'weather_api/current_weather.html', ctx)
