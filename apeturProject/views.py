from django.shortcuts import render
from .models import Photographer

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
    data = {
        'photographers': Photographer.objects.all()
    }
    return render(request, 'browse.html', data)
