from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('weather-multi-days/<str:location>/<int:day>', views.weather_multi_days_view, name='weather_api_weather_multi_days_view'),
]
