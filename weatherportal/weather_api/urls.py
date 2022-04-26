from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test1/', views.get_current_weather_by_location, name='weather_api_current_weather_view'),
    path('test2/<str:location>', views.weather_7_days_view, name='weather_api_weather_6_days_view'),
]
