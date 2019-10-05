from django.urls import path
from . import views

urlpatterns = [
    # homepage
    path('', views.home),

    # log in
    path('login', views.login),

    # sign up
    path('signup', views.signup),

    # browse
    path('browse', views.browse)
]
