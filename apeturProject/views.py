from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from django.shortcuts import redirect
from pathlib import Path
import simplejson as json
# User
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from datetime import datetime

# Forms
from . import forms

from urllib.request import urlopen, Request
from urllib.parse import urlencode

import requests
import base64

PAYPAL_CLIENT_SECRET = 'EHCVD1NeFbxNkp2RXv0LQ4Ynt1t16wTUZMvOCnJBhD9bKoNtIKoFvPfP8x13OmAI-PHGV2Xv3KOxT3Q6'
PAYPAL_CLIENT_ID = 'AYTN1WSX_5mo5aLm4M60lHLOCoBv2MbkCmp3LZf-8mA56YPQ2vyKrW3zxTZOZ234E1-aq_Zt0JG_TU7e'

convert_to_miles = 1.609

def payment(request):
        
    credentials = "%s:%s" % (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")

    headers = {
        "Authorization": ("Basic %s" % encode_credential),
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    param = {
        'grant_type': 'client_credentials',
    }
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    r = requests.post(url, headers=headers, data=param)

    print(r.text)
    context = {
        'PAYPAL_CLIENT_ID' : PAYPAL_CLIENT_ID,
        'auth_token' : r.text
    }

    return render(request, 'payment.html', context)

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
    if request.user.is_authenticated and request.method != 'GET' and 'plan' not in request.GET:
        return redirect('/')
    elif request.method == "POST":
        planSelected = request.POST.get('planSelected', None)

        # saveing the address
        address = None
        if planSelected is not None:
            streeAddress = request.POST.get('streeAddress', None)
            city = request.POST.get('city', None)
            state = request.POST.get('state', None)
            zipCode = request.POST.get('zipCode', None)
            country = request.POST.get('country', None)
            lat = request.POST.get('lat', None)
            lng = request.POST.get('lng', None)

            address = Address(zip_code=zipCode, country_sn=country,
                              state_sn=state, city_sn=city, latitude=lat, longitude=lng, street_address=streeAddress)
            address.save()

        # creating new user and client if the user isn't already logged in
        client = None
        if request.user.is_authenticated:
            client = request.user.client
            client.address = address
            client.save()
        else:
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
                        range(datetime.now().year - 122,
                              datetime.now().year),
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
                        'month_range': range(1, 13),
                        'date_range': range(1, 32),
                        'year_range': range(datetime.now().year - 122, datetime.now().year),
                        'signuperror': True,
                        'emailexists': True
                    },
                )

            user = User.objects.create_user(email, email, password)
            user.first_name = firstname
            dob = year + "-" + month + "-" + day
            user.save()
            client = Client(user=user, address=address, dob=dob)
            client.save()

            # log the user in
            username = get_user(email)
            user = authenticate(username=username, password=password)
            login(request, user)

        if planSelected is not None:
            photographer = Photographer(client=client)
            photographer.save()
            return redirect('/profile')


        return redirect('/')
    elif request.method == 'GET' and 'plan' in request.GET:
        is_photographer = False

        if request.user.is_authenticated:
            try:
                is_photographer = request.user.client.photographer is not None
            except Photographer.DoesNotExist:
                pass

        if is_photographer:
            return redirect('/')

        selectedPlan = request.GET.get("plan", 0)
        planName = 'free'
        planPrice = ''

        if selectedPlan == '1':
            planName = 'basic'
            planPrice = '$10'
        elif selectedPlan == '2':
            planName = 'Professional'
            planPrice = '$30'
        elif selectedPlan == '3':
            planName = 'Enterprise'
            planPrice = '$125'

        return render(
            request,
            'usermanagement/signup.html',
            {
                'month_range':
                range(1, 13),
                'date_range':
                range(1, 32),
                'year_range':
                range(datetime.now().year - 122,
                      datetime.now().year),
                'selected_plan': selectedPlan,
                'selected_plan_name': planName,
                'selected_plan_price': planPrice,
            }
        )
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
                range(datetime.now().year - 122,
                      datetime.now().year),
            },
        )


def photographer_signup(request):
    if request.user.is_authenticated:
        return render(request, 'usermanagement/photographer_signup.html')
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
    # if no user_id was passed as url parameter
    if request.method == 'GET' and 'user_id' in request.GET:
        user_id = request.GET['user_id']
        # check if user_id exist
        if user_id:
            user_id = int(user_id)
    else:
        # if user is not authenticated, redirect them to home
        if request.user.is_authenticated:
            # default user_id to current user's user id
            user_id = request.user.id
        else:
            return redirect('/')

    # Check for event form submission (creating an event) if not, create the form to pass to template
    if request.method == "POST":
        p_id = request.POST.get("p_id")
        photographer_name = photographer_name = Photographer.objects.filter(
            id=p_id).first().get_full_name()

        form = forms.CreateEvent(request.POST)
        if form.is_valid:
            event_date_string = request.POST.get(
                "event_date")  # Grab the event date
            c_id = request.POST.get("c_id")  # Grab client id
            # if client id does not exist ask for log in

            # grab schedule via date and photographer id
            schedule = Schedule.objects.filter(
                photographer_id=p_id, date=event_date_string)
            schedule = schedule.first()
            # schedule query returned an available schedule
            if schedule:
                # Create the event
                event_type = Event_Type.objects.filter(id = request.POST.get("event_type")).first()
                new_event = Event(event_type= event_type, schedule_id=schedule,client_id=c_id, start_time=request.POST.get("start_time"), end_time=request.POST.get("end_time"), confirmed = True)

                new_event.save()
    else:
        form = forms.CreateEvent()

    # Grab user data for according u_id
    user = User.objects.filter(id=user_id).first()
    user_name = user.get_short_name

    # Need to check profile type (client or photographer)
    if is_photographer(user_id):
        account_type = "Photographer"
        p_id = get_photographer_id_from_user_id(user_id)
    else:
        account_type = "Client"
        p_id = False

    # If photographer, grab schedule data needed

    gallery_images = settings.USER_FILE_URL + "0/featured-photo.jpg"
    followerCount = 12500000
    followingCount = 40000
    userQuote = 'Testing quote. Something very inspiring here. But let me just make it alot longer to test the text overflow'
    galleryMedia = [
        {
            'event_type': 'birthday',
            'url': settings.SITE_FILE_URL + "featured/birthday.jpg"
        },
        {
            'event_type': 'wedding',
            'url': settings.SITE_FILE_URL + "featured/wedding.jpg"
        },
        {
            'event_type': 'graduation',
            'url': settings.SITE_FILE_URL + "featured/graduation.jpg"
        },
        {
            'event_type': 'wedding',
            'url': settings.SITE_FILE_URL + "featured/wedding2.jpg"
        }
    ]
    reviews = [
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'stanley',
            'event_type': 'wedding',
            'event_date': datetime.strptime('2019-11-15', "%Y-%m-%d").date(),
            'comment': 'this is just a testing review form an imaginary user named stanley. But I need to make this comment much much longer for testing purpose. mainly to test the text overflow'
        },
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'martin',
            'event_type': 'birthday',
            'event_date': datetime.strptime('2019-11-01', "%Y-%m-%d").date(),
            'comment': 'It changed my life and now I am naming my first born after.'
        },
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'david',
            'event_type': 'wedding',
            'event_date': datetime.strptime('2019-10-10', "%Y-%m-%d").date(),
            'comment': 'I dont know about how the functionality work. for how it looks, its a five'
        },
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'jacob autrey',
            'event_type': 'wedding',
            'event_date': datetime.strptime('2018-09-15', "%Y-%m-%d").date(),
            'comment': 'very nice'
        },
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'jacob borilliar',
            'event_type': 'graduation',
            'event_date': datetime.strptime('2018-08-01', "%Y-%m-%d").date(),
            'comment': 'designed by complete garbage designer'
        },
        {
            'profile_pic': settings.USER_FILE_URL + '0/temp-profile-pic.jpg',
            'name': 'saul',
            'event_type': 'birthday',
            'event_date': datetime.strptime('2019-01-15', "%Y-%m-%d").date(),
            'comment': 'Smell like stanley'
        }
    ]

    photographerStat = {
        'portraits': 65,
        'wedding': 30,
        'birthday': 90
    }

    profileAbout = "testing text. more testing text. like I need a really really really long testing test for a profile about me section"

    return render(
        request,
        'profile.html',
        {
            'gallery_images': gallery_images,
            'follower_count': followerCount,
            'following_count': followingCount,
            'user_quote': userQuote,
            'gallery_media': galleryMedia,
            'reviews': reviews,
            'photographer_stat': photographerStat,
            'profile_about': profileAbout,
            'user_name': user_name,
            "schedule_json_data": retrieve_photographers_events_and_schedule(p_id)[1],
            "event_json_data": retrieve_photographers_events_and_schedule(p_id)[0],
            "account_type": account_type,
            "form": form,
            "p_id": p_id
        })


# schedule
def schedule(request):
    if request.method == "GET":
        p_id = request.GET.get("p_id", False)
      #  event_date = request.GET.get("date",False)
        photographer_name = ""
        if (p_id != False):
            photographer_name = Photographer.objects.filter(
                id=p_id).first().get_full_name()
    if request.method == "POST":
        p_id = request.POST.get("p_id")
        photographer_name = photographer_name = Photographer.objects.filter(
            id=p_id).first().get_full_name()

        form = forms.CreateEvent(request.POST)
        if form.is_valid:
            event_date_string = request.POST.get(
                "event_date")  # Grab the event date
            c_id = request.POST.get("c_id")  # Grab client id
            # if client id does not exist ask for log in

            # grab schedule via date and photographer id
            schedule = Schedule.objects.filter(
                photographer_id=p_id, date=event_date_string)
            schedule = schedule.first()
            # schedule query returned an available schedule
            if schedule:
                # Create the event
                # b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.') b.save()
                event_type = Event_Type.objects.filter(
                    id=request.POST.get("event_type")).first()
                new_event = Event(event_type=event_type, schedule_id=schedule, client_id=c_id, start_time=request.POST.get(
                    "start_time"), end_time=request.POST.get("end_time"), confirmed=True)
                new_event.save()
    else:
        form = forms.CreateEvent()
    data = {
        "schedule_json_data": retrieve_photographers_events_and_schedule(p_id)[1],
        "event_json_data": retrieve_photographers_events_and_schedule(p_id)[0],
        "p_name": photographer_name,
        "form": form,
        "p_id": int(p_id),
        "username": request.user.get_full_name()
    }
    return render(request, 'schedule.html', data)


# Account Settings
def account_settings(request):
    if request.user.is_authenticated:
        return render(request, 'usermanagement/account_settings.html')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
