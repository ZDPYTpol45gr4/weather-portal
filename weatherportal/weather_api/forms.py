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
    city_choice_field = forms.ChoiceField(choices=(), label='City')
    forecast_days_limit_choice_field = forms.ChoiceField(choices=DAYS, label='Select number of days it the forecast')

    def __init__(self, locations, *args, **kwargs):
        super(SelectCityForm, self).__init__(*args, **kwargs)
        self.fields['city_choice_field'].choices = locations
