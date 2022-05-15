import requests
import os
import datetime

from django.test import TestCase

from .views import get_location, get_actual_date, get_days_format

API_KEY = os.getenv('API_KEY')


class TestApiGetData(TestCase):
    def test_get_actual_date_return_good_date(self):
        date = get_actual_date()
        self.assertEqual(date, datetime.datetime.now())

    def test_get_days_format_return_good_data_names(self):
        DAYS_NAMES = (
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thirday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
        )
        data = get_days_format(8)
        for day in data:
            self.assertIn(day, DAYS_NAMES)

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
        self.assertEqual(data['lon'], server_output['lon'])
        self.assertEqual(data['country'], server_output['country'])
        self.assertEqual(data['name'], server_output['name'])
        self.assertEqual(data['state'], server_output['state'])
        self.assertIsNotNone(server_output['local_names'])

    def test_get_location_raises_exception(self):
        with self.assertRaises(ValueError):
            data = get_location('L234d')

