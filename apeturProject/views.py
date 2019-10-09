from django.shortcuts import render
from .models import Photographer
from django.conf import settings
from decimal import Decimal


def global_settings(request):
    # return any necessary values
    return {
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
    }


# homepage


def home(request):
    return render(request, 'home.html')


# log in
def login(request):
    return render(request, 'login.html')


# sign up
def signup(request):
    return render(
        request,
        'signup.html',
        {
            'month_range': range(1, 13),
            'date_range': range(1, 32),
            'year_range': range(1950, 2020)
        },
    )

# browse


def browse(request):
    if request.method == "GET":
        latitude = request.GET.get("lat",False)
        longitude = request.GET.get("lng",False)
        if latitude:
            latitude = round(Decimal(latitude),6)
        if longitude:
            longitude = round(Decimal(longitude),6)
        data = {
            "photographers" : Photographer.objects.all().filter(client__address__longitude = longitude, client__address__latitude = latitude),
            "lat" : latitude,
            "lng" : longitude
        }

    return render(request, 'browse.html',data)

