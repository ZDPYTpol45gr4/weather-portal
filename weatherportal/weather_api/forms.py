from django import forms
import os
import requests
from .models import CoordPoints, City

API_KEY = os.getenv('API_KEY')

DAYS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
)


class SelectCityForm(forms.Form):
    city_choice_field = forms.ModelChoiceField(queryset=CoordPoints.objects.none())
    forecast_days_limit_choice_field = forms.ChoiceField(choices=DAYS)

    def __init__(self, location, *args, **kwargs):
        self.base_fields['city_choice_field'].queryset = self.get_all_cities_names(location)
        super(SelectCityForm, self).__init__(*args, **kwargs)

    def get_all_cities_names(self, location):
        cities = self.get_location(location)
        print(cities)
        for city in cities:
            CoordPoints.objects.create(lat=float(city['lat']), lon=float(city['lon']), state=city['state'])
        return CoordPoints.objects.all()

    def get_location(self, location):
        response_location_coords = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={API_KEY}'
        )

        get_data_coords = response_location_coords.json()

        return get_data_coords
