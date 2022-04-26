from django.test import TestCase

from .views import get_location


class TestApiGetData(TestCase):
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
