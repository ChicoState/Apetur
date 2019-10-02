from django.shortcuts import render
from .models import Photographer

# Create your views here.

def home(request):
    return render(request, 'home.html')

def browse(request):
    data = {
        'photographers' : Photographer.objects.all()
    }
    return render(request,'browse.html',data)
