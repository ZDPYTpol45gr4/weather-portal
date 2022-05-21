from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('weather-multi-days/<str:location>/<int:day>', views.weather_multi_days_view, name='weather_api_weather_multi_days_view'),
    # path('weather-multi-days2/<slug:lat>/<slug:lon>/<int:day>', views.weather_multi_days_coords_view, name='weather_api_weather_multi_days_coords_view'),
    path('weather-form/<str:location>', views.cities_form_view)
]
