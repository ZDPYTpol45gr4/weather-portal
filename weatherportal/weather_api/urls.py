from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('weather-7-days/<str:location>', views.weather_7_days_view, name='weather_api_weather_7_days_view'),
]
