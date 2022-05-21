import datetime
import os
from pprint import pprint

import requests
import json
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect

from .data_classes import WeatherInfo
from .exceptions import exception_check, ServerResponseError
from .validators import Validator

from .forms import SelectCityForm
from .models import CoordPoints

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


def get_all_data_forecast_weather_by_coords(lat, lon):
    """
    Get weather data from api:
        Current weather
        Minute forecast for 1 hour
        Hourly forecast for 48 hours
        Daily forecast for 7 days
        National weather alerts
        Historical weather data for the previous 5 days
    """

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


def get_wather_by_coords(lat, lon):
    """
        Get weather by coordinates and validate data
    """
    data = get_all_data_forecast_weather_by_coords(lat, lon)
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


def cities_form_view(request, location):
    """
        Form allows user to choice city, cities can have same name in different location
    """
    if request.method == 'POST':

        form = SelectCityForm(location=location, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data['city_choice_field']
            lat, lon = data.lat, data.lon
            day = int(form.cleaned_data['forecast_days_limit_choice_field'])

            weather_forecast = get_wather_by_coords(lat, lon)
            data_out = weather_forecast.weather_data

            CoordPoints.objects.all().delete()

            ctx = {'data': data_out[:day], 'location': location, 'actual_date': datetime.datetime.now()}
            return render(request, 'weather_api/current_weather.html', ctx)
    else:
        form = SelectCityForm(location)
    ctx = {'form': form}
    return render(request, 'weather_api/form.html', ctx)
