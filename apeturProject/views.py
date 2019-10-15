from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from django.shortcuts import redirect
# User
from django.contrib.auth.models import User
from .models import Client
from .models import Photographer
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout


def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None


def global_settings(request):
    if request.user.is_authenticated:
        return {
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
            'USER_FIRST_NAME': request.user.get_short_name()
        }
    else:
        return {
            'GOOGLE_API_KEY': settings.GOOGLE_API_KEY
        }


# homepage
def home(request):
    notification_count = 14
    return render(request, 'home.html', {'notification_count': notification_count})


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
                return redirect('/')
            else:
                return render(request, 'login.html', {'loginerror': True})
        else:
            return render(request, 'login.html', {'loginerror': True})
    elif request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'login.html')


# log out
def logout_user(request):
    logout(request)
    return render(request, 'home.html')


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
                'signup.html',
                {
                    'month_range': range(1, 13),
                    'date_range': range(1, 32),
                    'year_range': range(1950, 2020),
                    'signuperror': True,
                    'passnotmatch': True
                },
            )

        username = get_user(email)
        if username is not None:
            return render(
                request,
                'signup.html',
                {
                    'month_range': range(1, 13),
                    'date_range': range(1, 32),
                    'year_range': range(1950, 2020),
                    'signuperror': True,
                    'emailexists': True
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
            'signup.html',
            {
                'month_range': range(1, 13),
                'date_range': range(1, 32),
                'year_range': range(1950, 2020),
            },
        )


# browse
def browse(request):
    if request.method == "GET":
        latitude = request.GET.get("lat", False)
        longitude = request.GET.get("lng", False)
        if latitude:
            latitude = round(Decimal(latitude), 6)
        if longitude:
            longitude = round(Decimal(longitude), 6)
        data = {
            "photographers": Photographer.objects.all().filter(client__address__longitude=longitude, client__address__latitude=latitude),
            "lat": latitude,
            "lng": longitude
        }

    return render(request, 'browse.html', data)
