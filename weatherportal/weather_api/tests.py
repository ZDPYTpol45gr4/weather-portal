import unittest.mock
import requests
import os

from django.test import TestCase
from nose.tools import assert_true


from .views import get_location

API_KEY = os.getenv('API_KEY')


class TestApiGetData(TestCase):

    def test_api_response_get_location(self):
        """Test location api response"""
        response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API_KEY}')

        assert_true(response.ok)

    def test_api(self):
        assert get_location()

    def test_api_response_get_weather_data(self):
        """Test weather api response"""
        response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API_KEY}')

        assert_true(response.ok)

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

        location = get_location('Lo324nd')
        self.assertEqual(location, None)
