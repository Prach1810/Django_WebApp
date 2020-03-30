import requests
from django.shortcuts import render,redirect
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=24da297ce45366c2ffc6ccf653028770'
    error = ''
    msg = ''
    msg_class = ''
    
    """
    city = 'Lucknow'

    r=requests.get(url.format(city))
    print(r.text)
    """
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error = 'City does not exist!'    
            else:
                error = 'City already exist!'
        if error:
            msg = error
            msg_class = 'is-danger'
        else:
            msg = 'City added successfully!' 
            msg_class = 'is-success'   

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r["main"]["temp"],
            'description' : r["weather"][0]["description"],
            'icon' : r["weather"][0]["icon"],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'msg' : msg,
        'msg_class' : msg_class
        }
    return render(request, 'weather/weather.html',context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
