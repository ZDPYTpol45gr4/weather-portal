import unittest.mock
import responses
import json

import requests
import os
#import pytest

from django.test import TestCase
#from nose.tools import assert_true
from http import HTTPStatus

from .views import get_location, get_weather, get_days_format
from .weather_data_class import WeatherInfo

API_KEY = os.getenv('API_KEY')


class TestApiGetData(TestCase):

    def test_api_response_get_location(self):
        """Test location api response"""
        response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API_KEY}')

        self.assertTrue(response.ok)

    def test_api_response_get_weather_data(self):
        """Test weather api response"""
        response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API_KEY}')

        self.assertTrue(response.ok)

    def test_get_location_properly(self):
        """
            Function get location from url, return data from weather api
        """

        location = get_location('London')

        msg = 'Test value is none'
        self.assertIsNotNone(location, msg)

    def test_get_location_with_wrong_location(self):
        """
            Fuction get location from url, location is wrong, api return empty data
        """

        self.assertRaisesMessage(ValueError, 'Empty data from getting location by location', get_location, 'Lo234n')


    def test_get_location_return_coords(self):
        data = {
            'name': 'Paris',
            'local_names': {},
            'lat': 48.8588897,
            'lon': 2.3200410217200766,
            'country': 'FR',
            'state': 'Ile-de-France'
        }

        server_output = get_location('Paris')
        self.assertEqual(data['lat'], server_output['lat'])


    def test_get_all_data_forecast_weather_by_location_return_dict_properly(self):
        data = {
            ''
        }