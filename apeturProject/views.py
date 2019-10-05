from django.shortcuts import render
from .models import Photographer


# homepage
def home(request):
    return render(request, 'home.html')


# log in
def login(request):
    return render(request, 'login.html')


# browse
def browse(request):
    data = {
        'photographers': Photographer.objects.all()
    }
    return render(request, 'browse.html', data)
