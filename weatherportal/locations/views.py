import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=Metric&appid=7cd4bf64a88cce70c2903d634e589f0f'

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            city_new = form.cleaned_data['name']
            city_number = City.objects.filter(name=city_new).count()

            if city_number ==0:
                rq = requests.get(url.format(city_new)).json()

                if rq['cod'] == 200:
                    form.save()
                else:
                    error_message = 'City is not existing in the real world'
            else:
                error_message = 'The city is already existing in the Weather-portal'

        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City added to the Weather-portal'
            message_class = 'is-success'

    form = CityForm()
    cities = City.objects.all()

    wt_data = []

    for city in cities:

        rq = requests.get(url.format(city)).json()

        weather_city = {
        'city' : city.name,
        'temperature' : rq['main']['temp'],
        'description' : rq['weather'][0]['description'],
        'icon' : rq['weather'][0]['icon'],
        }

        wt_data.append((weather_city))

    ctx = {'wt_data ' : wt_data, 'form' : form, 'message' : message, 'message_class' : message_class}
    return render(request, 'locations/locations.html', ctx)

def city_delete(request, city_name):
    City.objects.get(city_name).delete()
    return redirect('home')













