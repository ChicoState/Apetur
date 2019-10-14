from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Client, Photographer, Address
# Register your models here.

admin.site.register(Client)
admin.site.register(Photographer)
admin.site.register(Address)
