from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from django.shortcuts import redirect
from pathlib import Path
import simplejson as json
# User
from django.contrib.auth.models import User
from .models import Client
from .models import Photographer
from .models import find_photographer_in_radius
from .models import retrieve_photographers_schedules
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
import datetime

convert_to_miles = 1.609


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def global_settings(request):
    if request.user.is_authenticated:
        notification_count = 0

        return {
            "NOTIFICATION_COUNT": notification_count,
        }
    else:
        return {}


# homepage
def home(request):
    featured_images = [
        settings.SITE_FILE_URL + "featured/birthday.jpg",
        settings.SITE_FILE_URL + "featured/wedding.jpg",
        settings.SITE_FILE_URL + "featured/graduation.jpg",
        settings.SITE_FILE_URL + "featured/wedding2.jpg"
    ]
    tweets = [
        "I dont know what to write, but this is for testing any way.",
        "Another tweet that I am suppose to write for testing, but this one will be much longer.",
        "Dont know what the word limit is for twitter, but thats okay for now."
    ]
    instagram_images = [
        settings.SITE_FILE_URL + "featured/birthday.jpg",
        settings.SITE_FILE_URL + "featured/wedding.jpg",
        settings.SITE_FILE_URL + "featured/graduation.jpg",
        settings.SITE_FILE_URL + "featured/wedding2.jpg"
    ]
    return render(request,
                  'home.html',
                  {
                      'featured_images': featured_images,
                      'connect_tweets': tweets,
                      'connect_instagram': instagram_images
                  })


# log in
def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        username = get_user(email)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                nextParam = request.GET.get('next')
                if nextParam:
                    return redirect(nextParam)
                else:
                    return redirect('/')
            else:
                return render(request, 'usermanagement/login.html',
                              {'loginerror': True})
        else:
            return render(request, 'usermanagement/login.html',
                          {'loginerror': True})
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'usermanagement/login.html')


# log out
def logout_user(request):
    logout(request)
    return redirect('/')


# sign up
def signup_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == "POST":
        # get the inputs
        firstname = request.POST['firstname']
        month = request.POST['month']
        day = request.POST['day']
        year = request.POST['year']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password != repeatPassword:
            return render(
                request,
                'usermanagement/signup.html',
                {
                    'month_range':
                    range(1, 13),
                    'date_range':
                    range(1, 32),
                    'year_range':
                    range(datetime.datetime.now().year - 122,
                          datetime.datetime.now().year),
                    'signuperror':
                    True,
                    'passnotmatch':
                    True
                },
            )

        username = get_user(email)
        if username is not None:
            return render(
                request,
                'usermanagement/signup.html',
                {
                    'month_range':
                    range(1, 13),
                    'date_range':
                    range(1, 32),
                    'year_range':
                    range(datetime.datetime.now().year - 122,
                          datetime.datetime.now().year),
                    'signuperror':
                    True,
                    'emailexists':
                    True
                },
            )

        # creating the new user
        user = User.objects.create_user(email, email, password)
        user.first_name = firstname
        dob = year + "-" + month + "-" + day
        user.save()
        client = Client(user=user, dob=dob)
        client.save()

        # log the user in
        username = get_user(email)
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        return render(
            request,
            'usermanagement/signup.html',
            {
                'month_range':
                range(1, 13),
                'date_range':
                range(1, 32),
                'year_range':
                range(datetime.datetime.now().year - 122,
                      datetime.datetime.now().year),
            },
        )


def photographer_signup(request):
    # if request.user.is_authenticated:
    return render(request, 'usermanagement/photographer_signup.html')
    # else:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


# browse
def browse(request):
    if request.method == "GET":
        latitude = request.GET.get("lat", False)
        longitude = request.GET.get("lng", False)
        r = request.GET.get("r", False)
        r = float(r) * convert_to_miles
        if latitude:
            latitude = round(Decimal(latitude), 6)
        if longitude:
            longitude = round(Decimal(longitude), 6)
        if latitude != False and longitude != False:
            photographers = find_photographer_in_radius(latitude, longitude, r)

        else:
            photographers = (
                [], []
            )  # tuple of empty lists if nothing is returned from search
        data = {
            "photographers":
            photographers[0],  # first element in tuple is photographer objects
            "json_data":
            photographers[1],  # second element in tuple is json data
            "lat": latitude,
            "lng": longitude
        }

    return render(request, 'browse.html', data)


# profile
def profile(request):
    gallery_images = settings.USER_FILE_URL + "0/featured-photo.jpg"
    return render(
        request,
        'profile.html',
        {
            'gallery_images': gallery_images
        })
    return render(request, 'profile.html')


# schedule
def schedule(request):
    if request.method == "GET":
        p_id = request.GET.get("p_id", False)
        photographer_name = ""
        if (p_id != False):
            photographer_name = Photographer.objects.filter(
                id=p_id).first().get_full_name()
    data = {
        "json_data": retrieve_photographers_schedules(p_id),
        "p_name": photographer_name
    }
    return render(request, 'schedule.html', data)


# Account Settings
def account_settings(request):
    if request.user.is_authenticated:
        return render(request, 'usermanagement/account_settings.html')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


# Pricing
def pricing(request):
    return render(request, 'pricing.html')
