from django.shortcuts import render
import requests, environ
from .models import City
from .forms import CityForm

env = environ.Env()

environ.Env.read_env()

API_KEY = env("API_KEY")


# Create your views here.
def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format('{}', API_KEY)

    cities = City.objects.all()  # return all cities in the database

    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)  # add the data for the current city into the list

    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/index.html', context)  # returns the index.html template
