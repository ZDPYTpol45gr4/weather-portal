from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather_api.urls')),
    path('', include('register.urls')),
]
