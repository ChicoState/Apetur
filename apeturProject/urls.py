from django.urls import path
from . import views

urlpatterns = [
    # homepage
    path('', views.home),

    # log in
    path('login', views.login_user),

    # log out
    path('logout', views.logout_user),

    # sign up
    path('signup', views.signup_user),

    # photographer sign up
    path('photographer-signup', views.photographer_signup),

    # browse
    path('browse', views.browse),

    # profile
    path('profile', views.profile),

    # schedule
    path('schedule', views.schedule),

    # settings
    path('settings', views.account_settings)
]
