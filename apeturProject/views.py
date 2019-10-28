from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from django.shortcuts import redirect
from pathlib import Path
# User
from django.contrib.auth.models import User
from .models import Client
from .models import Photographer
from .models import find_photographer_in_radius
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
    return render(request, 'home.html')


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
        lastname = request.POST['lastname']
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
        user.last_name = lastname
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
    if request.user.is_authenticated:
        return render(request, 'usermanagement/photographer-signup.html')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


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
            photographers = []
        data = {
            "photographers": photographers,
            "lat": latitude,
            "lng": longitude
        }

    return render(request, 'browse.html', data)


# profile


def profile(request):
    return render(request, 'profile.html')
